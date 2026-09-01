#!/usr/bin/env python3
"""Exact-text synthetic readings or pitch-preserving slowdown of supplied masters."""
from pathlib import Path
import argparse
import array
import math
import shutil
import subprocess
import wave

from workbook import read_input, safe_name, save_json, sha


def run(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr[-4000:])
    return result


def audio_stats(file):
    result = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(file), '-f', 's16le', '-ac', '1', '-ar', '44100', '-'],
                            capture_output=True)
    if result.returncode:
        raise ValueError('Cannot decode audio: ' + str(file))
    samples = array.array('h', result.stdout)
    if len(samples) < 4410:
        raise ValueError('Empty or truncated audio: ' + str(file))
    rms = math.sqrt(sum(x * x for x in samples) / len(samples))
    if rms < 2:
        raise ValueError('Silent audio: ' + str(file))
    peak = max(abs(x) for x in samples)
    return {'duration_seconds': len(samples) / 44100, 'sample_rate': 44100,
            'rms_dbfs': 20 * math.log10(rms / 32768), 'peak_dbfs': 20 * math.log10(max(peak, 1) / 32768)}


def synthesize_baseline(data, language, folder):
    if not Path('/usr/bin/say').exists():
        raise RuntimeError('Local macOS speech service unavailable; select an approved native-language TTS engine.')
    conf = data.get('audio', {})
    voice = conf.get(language + '_voice', 'Meijia' if language == 'chinese' else 'Samantha')
    rate = conf.get(language + '_rate', 120 if language == 'chinese' else 125)
    voices = run(['/usr/bin/say', '-v', '?']).stdout
    if not any(line.startswith(voice + ' ') for line in voices.splitlines()):
        raise RuntimeError('Required voice unavailable: ' + voice + '; do not silently substitute another language.')
    lines = conf.get(language + '_spoken_lines', [x[language] + ('。' if language == 'chinese' else '') for x in data['lines']])
    folder.mkdir(parents=True, exist_ok=True)
    chunks = []
    for i, text in enumerate(lines, 1):
        raw, pcm = folder / f'line-{i:02d}.aiff', folder / f'line-{i:02d}.wav'
        run(['/usr/bin/say', '-v', voice, '-r', str(rate), '-o', str(raw), text])
        # say can exit zero with no samples in a sandbox; fail loudly here.
        audio_stats(raw)
        run(['ffmpeg', '-y', '-v', 'error', '-i', str(raw), '-af', 'atempo=0.9', '-ac', '1', '-ar', '44100', '-c:a', 'pcm_s16le', str(pcm)])
        with wave.open(str(pcm), 'rb') as w:
            chunks.append(w.readframes(w.getnframes()))
    assembled = folder / 'Baseline - Assembled.wav'
    with wave.open(str(assembled), 'wb') as w:
        w.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))
        w.writeframes(b'\x00\x00' * round(44100 * 0.4))
        for i, chunk in enumerate(chunks):
            w.writeframes(chunk)
            w.writeframes(b'\x00\x00' * round(44100 * (1.05 if i + 1 < len(chunks) else 1.3)))
    baseline = folder / 'Baseline - Master.wav'
    run(['ffmpeg', '-y', '-v', 'error', '-i', str(assembled), '-af', 'loudnorm=I=-19:TP=-2:LRA=7',
         '-ar', '44100', '-ac', '1', '-c:a', 'pcm_s16le', str(baseline)])
    return baseline, {'engine': 'macOS say', 'voice': voice, 'rate': rate, 'baseline_tempo': 0.9,
                      'baseline_line_gap_seconds': 1.05, 'synthetic': True}


def make_recordings(poem_path, chinese_master=None, english_master=None, speed=0.6, synthesize=False):
    if not 0.5 <= speed <= 2:
        raise ValueError('This renderer accepts tempo multipliers from 0.5 to 2.0.')
    poem_path = Path(poem_path).resolve()
    data = read_input(poem_path)
    output = poem_path.parent
    folder = output / 'Audio Sources'
    folder.mkdir(exist_ok=True)
    if not synthesize and (not chinese_master or not english_master):
        raise ValueError('Provide both exact-text masters, or explicitly select --synthesize.')
    results = []
    for language, supplied in [('chinese', chinese_master), ('english', english_master)]:
        spoken = data.get('audio', {}).get(language + '_spoken_lines', [x[language] for x in data['lines']])
        text_file = folder / ('Chinese - Spoken Text.txt' if language == 'chinese' else 'English - Spoken Text.txt')
        text_file.write_text('\n'.join(spoken) + '\n')
        if supplied:
            source = Path(supplied).resolve(strict=True)
            origin = {'engine': 'Pitch-preserving slowdown of supplied master', 'source': str(source),
                      'source_sha256': sha(source), 'synthetic': True,
                      'voice': data.get('audio', {}).get(language + '_voice', 'Meijia' if language == 'chinese' else 'Samantha')}
            # Preserve independently supplied audio in the edition, too.
            archived = output / 'Background' / 'Audio Masters'
            archived.mkdir(parents=True, exist_ok=True)
            target = archived / (language.capitalize() + ' - Reference Master' + source.suffix)
            if target.exists() and sha(target) != sha(source):
                raise ValueError('A different baseline is already preserved; create a new edition.')
            if source != target and not target.exists():
                shutil.copy2(source, target)
            origin['preserved_reference'] = str(target.relative_to(output))
        else:
            source, origin = synthesize_baseline(data, language, folder / (language.capitalize() + ' Baseline'))
        before = audio_stats(source)
        lang_label = 'Chinese Mandarin' if language == 'chinese' else 'English (' + data['translator'] + ')'
        name = safe_name(data['title_english'] + ' - ' + lang_label + ' - Slow Synthetic Reading')
        master = folder / (name + ' - Master.wav')
        mp3 = output / (name + '.mp3')
        if source == master or source == mp3:
            raise ValueError('Cannot slow an output onto itself; use the original baseline.')
        run(['ffmpeg', '-y', '-v', 'error', '-i', str(source), '-map', '0:a:0', '-af', f'atempo={speed}',
             '-ar', '44100', '-ac', '1', '-c:a', 'pcm_s16le', str(master)])
        after = audio_stats(master)
        expected = before['duration_seconds'] / speed
        if abs(after['duration_seconds'] - expected) > max(.15, expected * .005):
            raise ValueError('Unexpected slowed duration; check the tempo transform.')
        run(['ffmpeg', '-y', '-v', 'error', '-i', str(master), '-c:a', 'libmp3lame', '-b:a', '192k',
             '-metadata', 'title=' + data['title_english'], '-metadata', 'artist=' + data['poet_english'],
             '-metadata', f'comment=Synthetic reading; {speed * 100:g}% of reference speed; not historical exhibition audio.', str(mp3)])
        decoded = audio_stats(mp3)
        results.append({'language': language, 'origin': origin, 'tempo_multiplier': speed,
                        'expected_duration_seconds': expected, 'reference_audio': before, 'slowed_master': after,
                        'decoded_mp3': decoded, 'mp3': str(mp3.relative_to(output)),
                        'master': str(master.relative_to(output)), 'spoken_text': str(text_file.relative_to(output)),
                        'sha256': sha(mp3), 'pronunciation_listening_review': 'Not established by automated signal checks.'})
    report = {'kind': 'Synthetic readings, not the National Gallery exhibition recording',
              'tempo': f'{speed * 100:g}% of reference speed, applied once, pitch preserved', 'readings': results}
    save_json(folder / 'Recording Details.json', report)
    (output / 'Audio Recordings.md').write_text('# Audio recordings\n\nNew synthetic readings, not the historical exhibition audio.\n\n' +
        '\n'.join(f"- [{r['language'].capitalize()} — {r['slowed_master']['duration_seconds']:.1f} seconds](<{r['mp3']}>)" for r in results) +
        f'\n\nBoth play at {speed * 100:g}% of the reference speed, with pitch preserved. Chinese uses modern Mandarin; English uses {data["translator"]}\'s supplied wording.\n\n' +
        'WAV masters, exact spoken text and generation details are in `Audio Sources`. Automated duration and signal checks do not certify Mandarin pronunciation.\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--poem', required=True)
    parser.add_argument('--chinese-master')
    parser.add_argument('--english-master')
    parser.add_argument('--speed', type=float, default=0.6)
    parser.add_argument('--synthesize', action='store_true')
    args = parser.parse_args()
    report = make_recordings(args.poem, args.chinese_master, args.english_master, args.speed, args.synthesize)
    for r in report['readings']:
        print(f"{r['language']}: {r['slowed_master']['duration_seconds']:.2f}s — {r['mp3']}")


if __name__ == '__main__':
    main()
