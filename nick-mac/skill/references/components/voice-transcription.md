# Voice Transcription

Component: `voice-transcription`. Nick chose the captured FluidVoice setup as the initial baseline. Every later difference still uses the shared keep/adopt/new review process.

## Recorded standard

[standard.json](../../assets/fluidvoice/standard.json) captures the installed application version, portable preference overrides and settings using that version's defaults, app controls, and required model directories. [Vocabulary](../../assets/fluidvoice/parakeet_custom_vocabulary.json) captures the configured vocabulary rules. The dictionary is stored as decoded JSON within the preference snapshot.

The observed setup uses Parakeet TDT v3 speech recognition and local Fluid-1 enhancement. The source version's default dictation shortcut is Right Option in toggle mode; cancel is Escape. The saved configuration retains transcription/audio history with a 10 GB audio budget, enables debug logging, and disables analytics and automatic update checks. Preserve these choices unless Nick revises them through review.

These settings were checked against [FluidVoice's versioned settings implementation](https://github.com/altic-dev/FluidVoice/blob/v1.6.9/Sources/Fluid/Persistence/SettingsStore.swift) and [model downloader](https://github.com/altic-dev/FluidVoice/blob/v1.6.9/Sources/Fluid/Networking/ModelDownloader.swift). Effective defaults depend on application version.

## Inspect and plan

Run the comparison helper for `voice-transcription`. Compare the installed app version, portable preferences, dictionary/vocabulary, selected models and their readiness, login-item registration, shortcut, and input choice. Check microphone and accessibility permissions through the app/System Settings.

Use `voice-transcription:<domain>:<key>` preference IDs, `voice-transcription:app:version`, `voice-transcription:asset:vocabulary`, and `voice-transcription:control:<control-name>` for app controls. Microphone priority is expressed by function and peripheral name, never copied device identifiers: prefer the target's built-in input, followed by the recorded peripherals when present. If that input is unavailable, show alternatives in the plan.

A version difference is itself a decision. If Nick chooses a different version, inspect its effective defaults and migration behavior before applying this snapshot; do not blindly reset its settings. A downloaded folder does not prove the selected model is usable. On unsupported hardware, show the limitation and available alternatives rather than silently substituting an engine.

## Apply accepted choices

1. Update the standard artifacts for any values Nick adopts or newly defines. Preserve plist data types: a `plist_data_json` value in the snapshot represents JSON bytes in the application preferences.
2. For an accepted installation, use the [recorded release](https://github.com/altic-dev/FluidVoice/releases/tag/v1.6.9), or the different version Nick selected in the plan. Verify the app identity and installed version. Do not fetch an unspecified latest version as an equivalent.
3. Before changing target preferences, include a FluidVoice quit/relaunch in the plan and back up the affected domain and vocabulary. With the app closed, merge only approved preference changes using typed `defaults` writes or an exported domain merged and imported through `defaults`. Preserve every unmanaged key. Delete only accepted overrides whose chosen value is the applicable version's default. Do not wholesale import the reference machine's preference domain.
4. For accepted vocabulary changes, replace only the vocabulary configuration file under `~/Library/Application Support/FluidVoice/`, retaining a backup. Do not copy recordings or transcript/command history.
5. Relaunch FluidVoice. Configure microphone selection and login launch through the app; setting a saved preference alone does not register a login item. Download and activate only the selected speech/AI models through the app, as included in the plan. Grant device permissions through the normal macOS prompts.

## Verify

Recompare approved preferences and vocabulary, then verify the selected engines, model readiness, microphone, startup registration, and shortcut in the app. Test a short dictation and insertion into the intended destination without saving that test as standard data. A blocked permission, failed model, or unavailable UI test remains visible as incomplete.

Credentials, history contents, onboarding flags, analytics installation IDs, device identifiers, window geometry, and model weights are excluded from the standard artifacts. Their absence is not a request to delete target data.
