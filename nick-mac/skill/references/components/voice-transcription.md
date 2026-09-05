# Voice Transcription

Component: `voice-transcription`. Nick chose the captured FluidVoice setup as the initial baseline. Every later difference still uses the shared keep/adopt/new review process.

## Recorded standard

[standard.json](../../assets/fluidvoice/standard.json) captures application identity, portable preference overrides, observed effective settings, app controls, and required model directories. [Vocabulary](../../assets/fluidvoice/parakeet_custom_vocabulary.json) captures the configured vocabulary rules. The dictionary is stored as decoded JSON within the preference snapshot.

The observed setup uses Parakeet TDT v3 speech recognition and local Fluid-1 enhancement. The recorded dictation shortcut is Right Option in toggle mode; cancel is Escape. The saved configuration retains transcription/audio history with a 10 GB audio budget and enables local debug logging. The standard requires zero reporting and automatic update checks off. `ShareAnonymousAnalytics=false` is a stored preference, not evidence that all reporting has stopped.

## Mandatory zero-reporting requirement

Nick permits no FluidVoice reporting: no weekly/daily activity, usage analytics, telemetry, or automatic crash/diagnostic uploads, including reports from helper processes or the enhancement runtime. Local history and local debug logs may remain enabled without uploading them. Model downloads are a separate functional operation; permission to fetch assets does not permit reporting.

Before first launch, establish a mechanism that actually prevents all reporting. Inspect the actual application's reporting paths and controls, including scheduling, buffered reports, retry queues, helper processes, and login/relaunch behavior. If the supported settings cannot suppress all reporting, determine an effective app-scoped alternative and make its implementation and functional impact explicit in the alignment plan. Do not silently introduce a machine-wide network rule, modified build, or unrelated configuration change. Keep the application unlaunched unless reporting prevention is already in force; verification runs must also be protected from transmitting reports.

Verify both the control and its behavior: collect evidence that reporting cannot be sent, check all relevant reporting paths or enforced outbound controls, and observe attributable network activity during launch, idle, dictation, relaunch, and delayed-report/retry conditions. Account for weekly scheduling without changing the system clock or sending a test report. Check control persistence after login/relaunch and ensure later application updates cannot silently bypass it. Record the tested scope, mechanism, and any limits; a quiet short capture or an off switch alone is not proof of zero reporting.

Use `voice-transcription:control:reporting` for this requirement. The independent post-alignment sub-agent must verify it separately. If prevention or verification cannot be established, report FluidVoice blocked and keep it inactive; continue other accepted work. Residual reporting is not an alternative to offer Nick.

Source links in the standard document the implementation consulted during capture; they do not pin the installed application. `review_unset_preferences` identifies settings whose effective behavior still needs inspection, not a requirement to remove overrides. `effective_settings` records observed behavior to compare independently of how the app stores it. Model identities are configuration selections, not application release requirements.

## Inspect and plan

Run the comparison helper for `voice-transcription`. Separately inspect the mandatory `reporting_policy` in the standard; the helper does not prove reporting prevention. Compare app identity/presence, portable preferences, dictionary/vocabulary, selected models and their readiness, login-item registration, shortcut, and input choice. Check microphone and accessibility permissions through the app/System Settings.

Use `voice-transcription:<domain>:<key>` preference IDs, `voice-transcription:app:presence`, `voice-transcription:setting:<setting-name>`, `voice-transcription:asset:vocabulary`, and `voice-transcription:control:<control-name>` for app controls. Microphone priority is expressed by function and peripheral name, never copied device identifiers: prefer the target's built-in input, followed by the recorded peripherals when present. If that input is unavailable, show alternatives in the plan.

Compare effective behavior without collecting software versions. Inspect current settings before applying stored preferences; do not assume unset keys provide the desired behavior. A downloaded folder does not prove the selected model is usable. On unsupported hardware, show the limitation and available alternatives rather than silently substituting an engine.

## Apply accepted choices

1. Update the standard artifacts for any values Nick adopts or newly defines. Preserve plist data types: a `plist_data_json` value in the snapshot represents JSON bytes in the application preferences.
2. For an accepted installation, use the official [FluidVoice project](https://github.com/altic-dev/FluidVoice) distribution. Verify application identity without selecting or recording a software version. Consolidate any installation with the applications component in the combined plan.
3. Before changing target preferences, include a FluidVoice quit/relaunch in the plan and back up the affected domain and vocabulary. With the app closed, merge only approved preference changes using typed `defaults` writes or an exported domain merged and imported through `defaults`. Preserve every unmanaged key. Remove an override only if the accepted plan specifies it and the resulting effective behavior has been verified. Do not wholesale import the reference machine's preference domain.
4. For accepted vocabulary changes, replace only the vocabulary configuration file under `~/Library/Application Support/FluidVoice/`, retaining a backup. Do not copy recordings or transcript/command history.
5. Only after the mandatory reporting prevention above is in force, launch or relaunch FluidVoice. Configure microphone selection and login launch through the app; setting a saved preference alone does not register a login item. Download and activate only the selected speech/AI models through the app, as included in the plan. Grant device permissions through the normal macOS prompts.

## Verify

Recompare approved preferences and vocabulary, then verify the selected engines, model readiness, microphone, startup registration, and shortcut in the app. Test a short dictation and insertion into the intended destination without saving that test as standard data. A blocked permission, failed model, or unavailable UI test remains visible as incomplete.

Credentials, history contents, onboarding flags, analytics installation IDs, device identifiers, window geometry, and model weights are excluded from the standard artifacts. Their absence is not a request to delete target data.
