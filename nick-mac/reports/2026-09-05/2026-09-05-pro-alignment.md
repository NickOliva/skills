# Mac comparison and decisions — pro — 2026-09-05

**Pending or blank decision = no change.** Recommendations are proposals. The plan was approved on 2026-09-05; alignment and fresh independent review are complete for the agreed scope. Nick explicitly deferred the Stream Deck hardware test. Original comparison values below are retained as inspection history.

Inspection: repository commit `27d7d76`, baseline revision 5. Revision 6 added the optional Elgato/Corsair policy, mandatory zero reporting, and independent review. The approved alignment advances the standard to revision 8, including Nick’s later decision to turn AI enhancement off; implementation status is below.

## Alignment results

Implementation and the fresh independent review are complete for the agreed scope, with no actionable defects found. Nick explicitly deferred the Stream Deck hardware test. Backups: `~/Library/Application Support/Nick Mac/Backups/2026-09-05-pro/`.

| Ref | Result | Verification or limitation |
| --- | --- | --- |
| F1–F5 | Applied | All four Finder desktop options checked; Command-N opens Documents. |
| F6–F7 | Applied | Trim off in System Settings; Create PDF and the other four actions remain on. Stored ordering unchanged. Standard no longer compares numeric indexes. |
| T1 | Retained; standard updated | Fresh login shell loads the current theme and Git shortcuts. Shell files unchanged; theme asset captured. Native Terminal window visual check unavailable through automation. |
| V1 | Applied; implementation checks pass | Speech model active; Silero support model loaded successfully; microphone and Accessibility granted; actual launch-at-login registration on. Nick confirmed dictation and insertion with AI Off. AI prompt and editing shortcut remain off after relaunch; analytics/update checks off and analytics database absent. |
| A1 | Retained exception | Existing 1Password installation and baseline identity requirement preserved. |
| A2–A7 | Removed | All six app bundles are absent from Applications and present in the agreed recoverable backup; user data retained. |
| A8 | Removed | Final sweep: no remaining Citrix-owned package paths, seven known service registrations, processes, receipts, or named support folders. Known obsolete permissions reset; recoverable backups retained. |
| A9 | Retained; hardware test explicitly deferred by Nick | Elgato/Corsair unchanged, background activity off. Nick chose “Leave the hardware test for later.” Optional standard recorded. |
| B1–B3 | Applied | Three stale launch plists moved to backup; exact services unregistered. Valid Zoom helpers retained. |
| B4 | Retained; standard updated | Both effective telemetry opt-out values are `1`; combined task unchanged. |
| S1 | Applied | Repository duplicate link removed; global link and source retained. |
| W1 | Applied | Workflow moved to backup; Open in Codex absent from Finder folder menu. Other services retained. |
| C1 | Applied | Homebrew uninstall succeeded with automatic dependency cleanup disabled. |

FluidVoice reporting correction: the earlier blocker came from inspecting a different development snapshot. The installed official distribution corresponds to the [captured source](https://github.com/altic-dev/FluidVoice/blob/6f0684e694828b44fc643b7373f2a22d1e24eafa/Sources/Fluid/Analytics/AnalyticsService.swift), where `ShareAnonymousAnalytics=false` gates startup, activity recording, upload scheduling, and flushing, and purges queued analytics. It was set before first launch. Automatic update checks are also off. No firewall or modified app was installed.

Implementation test: compiled the corresponding analytics source with isolated database/settings fixtures and a network trap. Three fresh disabled instances recorded no activity or dictation analytics, created no upload timer/task, and made zero network attempts. A synthetic older queued event was purged on opt-out, and forced flush still made zero attempts. Test traffic was trapped and constrained to loopback; no report was sent. The real app has not created an analytics database after launch. After relaunch and successful dictation, analytics remains off and the database remains absent. A passive FluidVoice connection sample after model setup showed no connections; the source-level disabled-startup/queued-retry tests provide the delayed-report evidence. Automatic update checks are off; an externally replaced application would require a new privacy check. No full logout/login was performed: actual macOS login registration and app relaunch were verified.

Repository standard revision 8 records the approved Finder, prompt, workflow-exclusion, combined telemetry decisions, and AI enhancement Off. Original baseline revision 5 inspection below remains historical. All 12 bundled tests pass. Before/after comparison shows the five approved Finder settings and Trim availability changed, plus Finder navigation state from UI verification (`FXRecentFolders`, `GoToField`, `GoToFieldHistory`, and `NSWindow Frame GoToSheet`). Quick Action ordering and shell files are unchanged.

## Independent review — passed

Fresh reviewer `/root/final_alignment_review` independently reviewed the full revision-8 manifest, accepted plan, subsequent AI-Off decision, actual target state, functional evidence, and unintended changes. **Pass: no actionable defects found.** This reviewer made none of the changes. The earlier premature review does not count toward this result.

| Scope | Independent result |
| --- | --- |
| Finder and workflow | Pass; native UI confirms selected settings and removed action. |
| Terminal | Pass; fresh shell works, profiles and shell files unchanged. Native visual rendering remains unverified. |
| FluidVoice | Pass; AI prompt/editing off, speech models ready, permissions and actual login registration verified; successful dictation/insertion evidence confirmed. |
| Zero reporting | Pass for the installed implementation; matching source independently inspected, queued-report test rerun with zero network attempts, real analytics database absent, no current app connections. |
| Removals and retentions | Pass; Citrix cleanup and six app removals verified, selected retentions preserved. |
| Background tasks, skill scopes, Dapr | Pass; exact task changes and effective opt-outs verified. |
| Standard and unintended changes | Pass; revision 8 consistent, 12 tests pass, no unintended configuration changes found. |

Limits: Nick explicitly deferred Stream Deck hardware operation. No full logout/login or native Terminal visual test was performed; login registration, app relaunch, shell execution and unchanged profiles were checked. Previously undecided settings and broader helper-review candidates remain pending, not newly adopted requirements. The alternate 1Password identity remains the accepted exception. An external FluidVoice replacement requires a new privacy review.

Detailed evidence is preserved locally under `~/Library/Application Support/Nick Mac/Backups/2026-09-05-pro/final-independent-review/`.

## Approved plan

**Approved on 2026-09-05; applied with the subsequent AI-Off decision and explicit Stream Deck hardware-test deferral.** This plan implements the recorded decisions. Pending or blank items receive no change. V1 requires a verified method to prevent all reporting before activation; the other approved work proceeds independently.

| Ref | Change to this Mac | Change to the standard |
| --- | --- | --- |
| F1–F5 | Show hard disks, external disks, removable media, and connected servers on the desktop. Make new Finder windows open Documents. | Keep the selected baseline values and record acceptance. |
| F6–F7 | Disable the Trim Quick Action. Keep Create PDF enabled and preserve the relative order of the remaining actions. | Require Trim to be disabled; retire the obsolete Trim/PDF ordering requirement so it does not return as a difference. |
| T1 | Keep the current Terminal prompt and Git shortcuts. Open a fresh Terminal session to verify the captured setup. | Capture the current Oh My Zsh setup, `nick-mac` theme asset, and Git plugin selection as the standard. Do not copy unrelated startup-file contents. |
| V1 | Install/configure FluidVoice with AI enhancement Off and effective reporting prevention before first launch. Verify all reporting is blocked, including weekly activity, then verify speech models, dictation, and login behavior. | Require zero reporting, including weekly activity and helper/diagnostic uploads; independent verification is mandatory. AI enhancement is now Off by Nick’s subsequent decision; speech recognition remains required. |
| A1 | Keep 1Password exactly as it is. | Keep the existing identity requirement; record this target difference as intentionally ignored. |
| A2–A7 | Quit and uninstall MongoDB Compass, NETGEAR Switch Discovery Tool, Nitro, Postman, Realm Studio, and Remote Desktop. Preserve their user data and move app bundles to recoverable storage where supported. | Record these as removals selected for this target; do not turn them into an automatic removal rule for every Mac. |
| A8 | Uninstall Citrix Workspace and all Citrix-owned related components: login/background tasks, authentication and workspace helpers, Safari/browser integration, updater, USB helper, and Citrix-specific support/settings/cache files. | Record the target cleanup and its verification. |
| A9 | Keep Elgato Stream Deck and the Corsair helper. Leave the current background-activity switch unchanged. Nick subsequently explicitly deferred the physical monitor/Stream Deck test until later. | Optional, on computers Nick explicitly selects. No computer-name lists in the portable skill or standard. Policy updated; background activation remains unselected. |
| B1–B3 | Unload the stale Atlas updater and remove its plist. Remove the two stale user-installation Zoom updater/login-check plists. Preserve valid Zoom helpers and their current enabled/disabled choices. | Record the existing conditional cleanup policy as applied to these exact tasks. |
| B4 | Preserve both active ONNX Runtime and PowerShell telemetry opt-outs; verify their effective login-environment values. | Adopt this Mac’s combined opt-out task configuration. |
| S1 | Remove only `.agents/skills/nick-tool-cleanup`, the duplicate repository link. Retain the working machine-wide link and its source files. | Keep the declared machine scope; verify the duplicate is gone. |
| W1 | Move `Open in Codex.workflow` out of Finder Services into recoverable storage. | Record that this workflow is excluded and should not be installed by the standard. |
| C1 | Uninstall Homebrew’s `dapr-cli` package. Preserve project files and shared dependencies; do not run a general dependency cleanup. | Record the target removal. |

### FluidVoice: mandatory zero reporting

No reporting is permitted, including weekly activity, detailed analytics, telemetry, or automatic diagnostic uploads. Disabling detailed analytics alone is insufficient in implementations that retain weekly activity reporting. The installed implementation’s native opt-out was separately traced and tested, as documented above. There is no consent question to revisit.

The implementation must establish effective prevention before first launch, cover scheduled reports, retries, relaunch/login, and helpers, and pass independent verification. FluidVoice is installed and running with reporting prevention configured before its first launch and checked against the matching source. Any additional control and its functional impact must be made concrete in this plan before use. If prevention cannot be established, keep FluidVoice inactive and report it blocked.

Once the plan is accepted and reporting prevention is established, use the official project distribution/Homebrew cask, configure Parakeet speech recognition with AI enhancement off, download its required speech models, and apply the full stored baseline. The intended setup includes Right Option toggle dictation, Escape cancellation, AI editing shortcut disabled, clipboard-free insertion, the saved vocabulary/dictionary, history/audio retention with a 10 GB audio budget, debug logging on, and automatic update checks off. Use a built-in microphone when available; if unavailable, bring back the actual input choices instead of silently selecting another device. The project documents several GB of model storage and requires microphone and Accessibility permissions for dictation/insertion. No paid subscription, cloud provider, API key, or account setup is included. [Official setup instructions](https://github.com/altic-dev/FluidVoice#quick-start)

### Backups, interruptions, and verification

- Back up replaced settings, workflows, plists, and Citrix-owned configuration locally under `~/Library/Application Support/Nick Mac/Backups/2026-09-05-pro/`, outside Git and skill-discovery folders. Keep the removed app bundles recoverable where supported. Preserve other applications’ documents/data and do not empty Trash.
- Use the available [Citrix vendor uninstaller](https://docs.citrix.com/en-us/citrix-workspace-app-for-mac/install-uninstall.html#using-the-terminal-command), then check for and remove verified Citrix-owned leftovers. System-wide cleanup may require administrator authentication. Any active Citrix sessions must end; stop for unsaved-work prompts rather than discarding work.
- Quit applications being removed. Finder may need a relaunch to refresh menus. FluidVoice, only with reporting prevention in force, will be opened/relaunched and will present microphone/Accessibility permission prompts. No full-computer restart is scheduled; if an installer/uninstaller requires one, report it before restarting.
- Recheck settings, app identities, exact launch registrations, related processes, Finder actions, and skill links. Test a new Finder window and Terminal prompt. Test FluidVoice model readiness, login registration, microphone, dictation, and text insertion if installed. Verify Stream Deck through the monitor when connected; unavailable hardware remains a reported manual check.
- After implementation checks, a separate sub-agent that made none of the changes must review the full manifest and accepted plan, verify actual behavior and zero reporting, check retentions/removals and unintended changes, and record evidence and pass/fail/unverified results here. The implementing agent fixes findings within scope; the reviewer rechecks them. An incomplete review cannot be reported as complete alignment.
- Update standard artifacts, manifest decisions/revision, portable decision notes, and the result in this report together. Keep the original inspection evidence. Run the skill’s tests if its comparison logic changes to handle the newly excluded actions. Do not commit or push as part of applying this plan.

The other settings and candidates without a specific decision stay as they are. Postman Agent has no removal decision and remains installed; it is separate from the selected Postman application. Earlier background-registry inspection was incomplete, so cached UI records will not be treated as active software without checking their paths and service state.

## Review table

| Ref | Item | Baseline | This Mac | Recommendation | Decision |
| --- | --- | --- | --- | --- | --- |
| F1 | Hard disks on desktop | Shown | Hidden | Show them, as you selected. | Accept baseline — show hard disks on the desktop. |
| F2 | External disks on desktop | Shown | Hidden | Show them, as you selected. | Accept baseline — show external disks on the desktop. |
| F3 | Removable media on desktop | Shown | Hidden | Show them, as you selected. | Accept baseline — show removable media on the desktop. |
| F4 | Connected servers on desktop | Shown | Hidden | Show them, as you selected. | Accept baseline — show connected servers on the desktop. |
| F5 | Where new Finder windows open | Documents | Computer, showing disks and volumes | Open Documents, as you selected. | Accept baseline — new Finder windows open Documents. |
| F6 | Create PDF position | Listed after Trim | Listed before Trim | Keep Create PDF enabled; retire the PDF-versus-Trim ordering question. | No ordering change needed after removing Trim; keep Create PDF enabled. |
| F7 | Trim audio/video Quick Action | Enabled | Enabled | Disable Trim here and in the standard, as you selected. Keep the macOS component installed. | Remove Trim from this Mac’s Quick Actions and from the standard. |
| T1 | Terminal prompt and Git shortcuts | No verified replacement prompt is defined | Customized prompt with the current folder, Git branch/change information, and Git shortcuts, provided by Oh My Zsh | Keep this setup and record it as the standard; no change to this Mac’s prompt. | Adopt this Mac’s current Terminal prompt and Git shortcuts as the standard; keep this Mac’s setup. |
| V1 | FluidVoice dictation | Required with the recorded speech models, shortcuts, and settings | App and required models were absent at inspection | Configure local speech recognition, AI enhancement Off, and zero reporting; verify dictation and insertion. | Accept baseline with zero reporting. Subsequent decision: turn AI enhancement and AI editing shortcut off here and in the standard. |
| A1 | Which 1Password installation satisfies the standard | Requires one specific application identifier | 1Password is installed and running under a different identifier | Accept the installed 1Password identity and revise the baseline identity requirement; leave this installation in place. | Ignore — keep the installed 1Password and the baseline identity requirement unchanged. |
| A2 | MongoDB Compass | Not part of the adopted standard | Installed | Uninstall the application, preserving user data. | Remove from this Mac. |
| A3 | NETGEAR Switch Discovery Tool | Not part of the adopted standard | Installed | Uninstall the application, preserving user data. | Remove from this Mac. |
| A4 | Nitro | Not part of the adopted standard | Installed | Uninstall the application, preserving user data. | Remove from this Mac. |
| A5 | Postman | Not part of the adopted standard | Installed | Uninstall the application, preserving user data. | Remove from this Mac. |
| A6 | Realm Studio | Not part of the adopted standard | Installed | Uninstall the application, preserving user data. | Remove from this Mac. |
| A7 | Remote Desktop | Not part of the adopted standard | Installed | Uninstall the application, preserving user data. | Remove from this Mac. |
| A8 | Citrix and all related components | Not part of the adopted standard | Citrix Workspace plus seven launch-agent/daemon entries and related helpers are present | Remove Citrix Workspace and its related login items, background services, browser integration, updater, USB helper, and Citrix-specific support files. | Remove everything related to Citrix from this Mac. |
| A9 | Elgato Stream Deck and Corsair helper | Optional; Nick selects targets individually | Stream Deck is installed; Corsair background activity is off | Keep on this selected Mac and verify operation through the monitor when available. Do not require them on other computers. | Keep here. Optional elsewhere; Nick will specify computers. No computer-name lists in the portable skill. Hardware test explicitly deferred until later. |
| B1 | Stale Atlas updater | Remove updater tasks when their app is absent | Task still tries to launch an updater for the missing Atlas app | Unload this exact task and move its plist to a recoverable backup. | Accept recommendation — unload the stale Atlas updater and move its plist to a recoverable backup. |
| B2 | Stale Zoom user updater | Remove tasks pointing to an absent installation | Updater points to missing Zoom under the user Applications folder | Move this stale plist to a recoverable backup; retain helpers for the installed Zoom app. | Accept recommendation — remove the stale user Zoom updater plist; retain valid Zoom helpers. |
| B3 | Stale Zoom user login check | Remove tasks pointing to an absent installation | Login check points to the same missing user installation | Move this stale plist to a recoverable backup; retain helpers for the installed Zoom app. | Accept recommendation — remove the stale user Zoom login-check plist; retain valid Zoom helpers. |
| B4 | Telemetry opt-outs at login | Sets the ONNX Runtime opt-out | Sets both ONNX Runtime and PowerShell opt-outs; both are active | Keep both opt-outs and adopt this implementation into the standard. | Accept recommendation — keep both active telemetry opt-outs and adopt this implementation as the standard. |
| S1 | Duplicate nick-tool-cleanup installation link | One machine-wide link | Machine-wide and repository links both load the same skill | Remove only the extra repository link; retain the machine-wide link and skill source. | Accept recommendation — remove the extra repository link; retain the machine-wide link and skill source. |
| W1 | Open in Codex Finder action | No adopted workflow yet | Calls missing Codex.app; the installed application is ChatGPT.app | Repair the action to use the installed app and verify it opens the selected folder. Leave adoption into the standard for a separate choice. | Remove Open in Codex from Finder and exclude it from the standard; do not repair it. |
| C1 | Dapr CLI | Not part of the adopted standard | Installed through Homebrew as `dapr-cli` | Uninstall `dapr-cli`; preserve project files and shared dependencies. | Remove from this Mac. |

<details>
<summary>Original inspection findings and evidence — before alignment</summary>

## Finder

The seven stored baseline differences are F1–F7. The four desktop visibility flags and new-window selection were checked in Finder Settings. List view, path bar, status bar, automatic Trash removal after 30 days, and opening folders in separate windows match the stored baseline. All six recorded native Quick Actions are enabled; System Settings also shows six enabled System Services extensions. PDF/Trim ordering differs in stored preferences.

Effective settings without an adopted baseline value: **show all filename extensions is off** and **warn before changing an extension is on**, verified in Finder Settings. Hidden-file visibility remains unverified; the override is unset and was not treated as proof of a default.

The bundled **open in vs code** workflow exactly matches the installed files; VS Code is present. **Copy Path** and **Open in Codex** are present and visible in a folder context menu. Copy Path’s executable helper exists. The baseline’s `Copy path.workflow` candidate corresponds to the current differently capitalized `Copy Path.workflow`; neither candidate has an adopted workflow asset. `Send to Kindle.workflow` is absent, although the Send to Kindle application is installed. No service was executed, so end-to-end behavior remains untested.

Other visible folder services include Compare Folders, Select Left Folder for Compare, New Terminal at Folder, New Terminal Tab at Folder, Folder Actions Setup, and Reveal in Windows. These are review candidates, not adopted requirements. Native image/PDF/video action visibility remains dependent on selected file type; no media-operation test was run.

Follow-up inspection: the Services submenu threshold (`NSServicesMinimumItemCountForContextSubmenu`) is explicitly **20** on this Mac. It controls Services grouping and is separate from native Quick Action ordering; it has not been adopted into the standard. This remains an open review candidate.

Additional observed settings available for a future baseline decision: warn before removing from iCloud Drive on; warn before emptying Trash on; keep folders on top off both in windows and on the desktop; Finder searches default to This Mac. None has been adopted.

## Terminal and shell

The Terminal window’s recorded appearance settings already match on this Mac. **T1 concerns the command prompt—the text and symbols beside where you type commands—and its command shortcuts.**

This Mac’s configuration provides:

- A current-folder display in blue and a `▶` prompt on the next line.
- In a Git repository, information such as the branch, whether files have changed, and time since the last commit.
- Git command shortcuts supplied by an add-on called **Oh My Zsh**. The selected appearance is named `nick-mac`.

These features are configured in the inspected files; a fresh Terminal session was not launched to verify their rendering. The shell is zsh, not csh. Oh My Zsh is the customization add-on; it is not a different Terminal application.

**What the baseline actually establishes:** its author recorded that no customization was found in the files inspected. It does not describe or demonstrate what prompt you would get instead. My earlier “no framework/theme override” wording made that incomplete observation sound like a clear alternative to adopt. It is not sufficient grounds to remove your current setup.

**T1 asks: should this Mac’s current Terminal prompt and Git shortcuts become the standard?**

- **Use this Mac’s setup as the standard:** keep the prompt and shortcuts here, and record the setup for future Mac alignment plans.
- **Choose a different setup:** first specify and preview the prompt and shortcuts you want; no replacement is currently defined.
- **Leave undecided:** keep this Mac as it is and leave the standard unresolved.

T1 decision: adopt this Mac’s current prompt and Git shortcuts as the standard. The standard update is recorded but not yet applied; no change to this Mac’s prompt is requested. The matching Terminal window/profile settings do not require action.

## FluidVoice

FluidVoice was not found in system/user application directories, nested application folders, or the Spotlight bundle-ID search; direct app resolution also failed. Its preference domain and vocabulary file were absent. The three expected model directories were absent: Parakeet TDT speech recognition, Silero VAD, and Fluid-1 local enhancement.

The helper emitted 30 missing persisted/app/asset comparisons and 70 unset-preference checks. These stem from the absent setup and **are not 100 independent effective-behavior failures**. The 22 app-control/effective-setting checks and model readiness cannot be exercised until the app exists.

If you retain this baseline, a later plan needs FluidVoice installation from its official project, the selected model downloads, microphone/accessibility permission prompts, login registration, microphone choice, and a dictation/insertion test. The baseline calls for Right Option toggle dictation, Escape cancellation, Option+R editing, Parakeet speech recognition with Fluid-1 enhancement, local vocabulary, retained transcript/audio history with a 10 GB audio budget, debug logs on, analytics off, and automatic update checks off. Input should prefer a built-in microphone, then the recorded display/Teams inputs if available; input availability and permissions remain unverified.

The complete recorded stored values and app-control expectations are included in the appendix. No absent override was assumed to implement the baseline.

## Applications

**18 of 20 required exact bundle identities are present.** FluidVoice is absent; 1Password is present under an alternate identity (A1). The latter is an identity-policy question, not a release comparison. Optional apps: Slack present; Keynote, Numbers, and OneDrive absent. Their optional status permits either presence or absence.

| Application | Baseline | Observed |
| --- | --- | --- |
| 1Password | required | Alternate identity installed; see A1 |
| Amazon Kindle | required | present |
| ChatGPT | required | present |
| Day One | required | present |
| Developer | required | present |
| Docker | required | present |
| Dropbox | required | present |
| FluidVoice | required | absent |
| Google Chrome | required | present |
| Keynote | not-required | absent |
| Microsoft Excel | required | present |
| Microsoft PowerPoint | required | present |
| Microsoft Teams | required | present |
| Microsoft Word | required | present |
| Numbers | not-required | absent |
| Obsidian | required | present |
| OneDrive | not-required | absent |
| Pages | required | present |
| Safari | required | present |
| Slack | not-required | present |
| TestFlight | required | present |
| Visual Studio Code | required | present |
| Xcode | required | present |
| zoom.us | required | present |

The manifest leaves **19 required-app configurations awaiting review**; installation alone does not make those applications fully aligned. Safe portable settings sampled during this run: Safari shows full URLs and has the Develop menu enabled. Docker has autostart off, analytics off, automatic update disabling on, Apple virtualization and VirtioFS on, Kubernetes off, 7 CPUs and 25,088 MiB memory allocated. Resource allocation is a target observation, not a portable requirement. Other app settings have no defined baseline and were not comprehensively audited; no settings were inferred from absence.

### Additional installed applications — inclusion candidates

The following user applications were outside the manifest at inspection. Nick has selected MongoDB Compass, NETGEAR Switch Discovery Tool, Nitro, Postman, Realm Studio, and Remote Desktop for removal (A2–A7). Citrix and all related components are also selected for removal (A8). Elgato Stream Deck and its Corsair helper are selected for retention here and optional inclusion on other targets Nick explicitly selects (A9). These decisions are recorded but not yet applied; other inclusion choices remain open. Related support utilities are separated below.

Adobe Lightroom Classic, Adobe Photoshop, Anki, Arduino IDE, Beyond Compare, Citrix Workspace, Civ6, CivilizationVII, Claude, Creative Cloud, Creative Cloud Desktop App, DB Browser for SQLite, DWS, DbSchema, Elgato Stream Deck, Evernote, Final Cut Pro, FuelClock, Google Drive, Kindle, Kindle Create, Kindle Previewer, Microsoft OneNote, MongoDB Compass, NETGEAR Switch Discovery Tool, Nitro, Parallels Desktop, Postman, PowerShell, Quicken, Realm Studio, Remote Desktop, SF Symbols beta, Send to Kindle, SideQuest, Sonos, The Unarchiver, Thunderbird, Uninstall Send to Kindle, WdDesk, WhatsApp, organize.

**Supporting apps, shortcuts, installers, or diagnostic utilities:** Adobe Creative Cloud Diagnostics, CCXProcess, Core Sync, Creative Cloud Helper, Creative Cloud Installer, Creative Cloud UI Helper, Creative Cloud UI Helper (GPU), Creative Cloud UI Helper (Renderer), Creative Cloud Uninstaller, DbSchema Uninstaller, Google Docs, Google Sheets, Google Slides, IDLE, Postman Agent, Python Launcher, USB File Manager. Their presence does not independently establish that each should be a build requirement.

### Command-line tools — inclusion candidates

Homebrew receipt flags identify the following as explicitly requested installations. Nick has selected Dapr CLI (`dapr-cli`) for removal (C1); it has not yet been uninstalled. Other tools remain review candidates:

azure-cli, bash-completion, dapr-cli, evernote-backup, fd, ffmpeg, gh, helm, jq, msodbcsql18, mssql-tools, nmap, node, pandoc, poppler, python, ripgrep, tfenv, weasyprint, xcodegen, yq, zsh, zsh-completions.

Other discovered command/tool families include AWS CLI, Docker/Compose and its credential helpers, kubectl, PowerShell, MongoDB shell, npm/pnpm/Yarn, Angular and Nest tooling, Codex CLI, VS Code CLI, Parallels utilities, Kindle Previewer utilities, and the local Copy Path helper. Presence was inspected without executing tools or comparing releases. Package dependency receipts and aliases were not promoted into separate requirements. Homebrew has 99 distinct supporting-or-unspecified formula names after identity normalization; these include media codecs, font/rendering libraries, TLS/crypto libraries, Python support, and database libraries. Local project dependencies and every possible custom executable directory were not exhaustively inventoried.

## Login items and background tasks

System Settings shows **Dropbox** as the Open at Login item. Background switches and launch registration were inspected separately; an allowed switch does not establish a running process, and a disabled switch does not mean the app is uninstalled.

| Baseline policy | Observed evidence | Result |
| --- | --- | --- |
| Atlas | Stale AtlasUpdateHelper path; service loaded, spawn scheduled, exit 78; no related process found | B1: cleanup candidate, awaiting approval. |
| Zoom | Two stale user plists; valid system-application Zoom updater executables and ZoomDaemon executable exist; Zoom background groups off; checked updater services not loaded | B2/B3: stale candidates. Keep/enable/disable valid helpers needs a separate choice; current off state was preserved. |
| Telemetry opt-out (ONNX Runtime) | User task loaded, completed with exit 0. Unsandboxed launchctl verifies ORT_DISABLE_TELEMETRY=1 and POWERSHELL_TELEMETRY_OPTOUT=1 | ONNX functional setting matches; expanded implementation differs (B4). This does not prove every application honors the variables. |
| Docker helpers | Docker background group on; com.docker.helper registered. No vmnetd/socket privileged executable at standard helper locations; no Docker process at sample time | Not automatically a defect. Current Docker configuration must determine privileged-helper need; do not install historical helpers merely to match a list. |
| Retained app helpers | Dropbox updater valid and registered. Google updater and Microsoft AutoUpdate binaries exist but background groups off; 1Password background group off. Teams/Office licensing registration not fully verified | Review current background choices; no blanket enabling. Office licensing and Teams helper coverage remains incomplete. |
| OneDrive leftovers | No OneDrive app, known launch plist/content target, related registered service, or OneDrive/SyncReporter process found in inspected locations | No OneDrive cleanup proposed. Full cached registry records were unavailable. |

| UI background group | Observed |
| --- | --- |
| 1Password | Off |
| Adobe Creative Cloud | Off |
| AMZN Mobile LLC | Off |
| Citrix Systems, Inc. | On |
| Citrix Workspace | Off |
| Corsair Memory, Inc. — Elgato Stream Deck background helper | Off at inspection; retain with Stream Deck under A9 |
| Docker | On |
| DropboxUpdater | On |
| Google LLC | Off |
| Google Updater | Off |
| Microsoft AutoUpdate | Off |
| OpenAI, L.L.C. | On |
| sh (custom telemetry task) | On |
| Weather | On |
| Zoom | Off |
| zoom.us | Off |

Citrix Workspace and all related components are now selected for removal (A8), including ServiceRecords, SafariAdapter, AuthManager, Workspace Helper, WorkspaceHelperDaemon, its updater, and USB helper. Elgato Stream Deck and its Corsair helper are selected for retention under A9. They are optional; Nick will specify which computers use them. Monitor connection alone does not make them required. Current background activity was off; verify the monitor connection and app operation during alignment before deciding whether background activation is needed. Other background candidates include Adobe Creative Cloud/CCXProcess and Kindle Previewer’s helper. Their executable paths resolve to installed software. Citrix SafariAdapter is running; its AuthManager and WorkspaceHelper daemon are registered but not running. Adobe CCXProcess has both user and system-wide agent plist entries; neither was loaded in the checked user domain, so duplicate filenames alone do not justify deletion. Seven Google/Dropbox legacy plist files are empty dictionaries, with no label or executable; they are not active executable task definitions and no cleanup was applied.

## Nick skill installations

Eight declared installations match. `nick-tool-cleanup` has the duplicate scope finding S1. `nick-money` has requirements but no implemented skill and is correctly reported as pending implementation; no empty installation should be created. No Nick Mac disabled-skill entry was found in the local Codex configuration, and no additional Nick Mac link was found in the two other known skill checkouts inspected.

| Skill | Declared scope | Result |
| --- | --- | --- |
| build-employment-opportunity-dossier | machine | matches recorded value |
| chinese-poem-workbook | machine | matches recorded value |
| email-operations | machine | matches recorded value |
| nick-coach | machine | matches recorded value |
| nick-guided-srs | repo | matches recorded value |
| nick-mac | repo | matches recorded value |
| nick-money | machine | source not built |
| nick-museums | repo | matches recorded value |
| nick-tool-cleanup | machine | review installation difference |
| test-elementary-knowledge | machine | matches recorded value |

## Verification limits

- `sfltool dumpbtm` failed authorization in the sandbox; an unsandboxed retry produced no output and was cancelled. System Settings supplied current login/background switch evidence, supplemented by plist contents and targeted launchctl checks. Complete cached BTM records and provenance were not available. No security prompt was bypassed.
- Sandbox `launchctl getenv` returned empty values; those were not treated as missing opt-outs. Unsandboxed reads subsequently confirmed both values are `1`.
- FluidVoice effective settings, models, microphone/accessibility permissions, startup registration, and dictation behavior cannot be verified while it is absent.
- Finder hidden-file effective state and file-type-specific Quick Action behavior remain untested; inspected workflows were not run. A new Terminal session was not launched.
- Most application settings have no defined baseline. Presence checks, selected portable setting observations, and known background helpers do not constitute complete configuration audits of every installed app.
- App search covered common system/user roots and nested app directories, plus Spotlight for missing required identities. Tool discovery covered Homebrew receipts and common user/system executable directories. Skill discovery covered the helper’s machine/repo/ancestor roots and two known relevant skill checkouts; arbitrary unindexed locations were not exhaustively searched.


## Appendix — item-level evidence

The following tables preserve the baseline’s stable IDs. “Matches stored value” establishes the comparison shown, not all runtime behavior. The supplemental findings above take precedence over the helper’s initial missing-app or unset-setting labels.

### Finder and Terminal stored comparisons

| Stable ID | Recorded | Observed | Result |
| --- | --- | --- | --- |
| finder:com.apple.finder:FXPreferredViewStyle | Nlsv | Nlsv | Matches stored value |
| finder:com.apple.finder:ShowPathbar | On | On | Matches stored value |
| finder:com.apple.finder:ShowStatusBar | On | On | Matches stored value |
| finder:com.apple.finder:ShowHardDrivesOnDesktop | On | Off | Difference |
| finder:com.apple.finder:ShowExternalHardDrivesOnDesktop | On | Off | Difference |
| finder:com.apple.finder:ShowRemovableMediaOnDesktop | On | Off | Difference |
| finder:com.apple.finder:ShowMountedServersOnDesktop | On | Off | Difference |
| finder:com.apple.finder:FXRemoveOldTrashItems | On | On | Matches stored value |
| finder:com.apple.finder:FinderSpawnTab | Off | Off | Matches stored value |
| finder:com.apple.finder:NewWindowTarget | PfDo | PfCm | Difference |
| finder:pbs:FinderActive/APPEXTENSION-com.apple.finder.CreatePDFQuickAction | On | On | Matches stored value |
| finder:pbs:FinderActive/APPEXTENSION-com.apple.finder.MarkupQuickAction | On | On | Matches stored value |
| finder:pbs:FinderActive/APPEXTENSION-com.apple.finder.RotateQuickAction | On | On | Matches stored value |
| finder:pbs:FinderActive/APPEXTENSION-com.apple.finder.TrimQuickAction | On | On | Matches stored value |
| finder:pbs:FinderActive/is.workflow.actions.image.convert.finder | On | On | Matches stored value |
| finder:pbs:FinderActive/is.workflow.actions.image.removebackground | On | On | Matches stored value |
| finder:pbs:FinderOrdering/APPEXTENSION-com.apple.finder.CreatePDFQuickAction | 3 | 2 | Difference |
| finder:pbs:FinderOrdering/APPEXTENSION-com.apple.finder.MarkupQuickAction | 1 | 1 | Matches stored value |
| finder:pbs:FinderOrdering/APPEXTENSION-com.apple.finder.RotateQuickAction | 0 | 0 | Matches stored value |
| finder:pbs:FinderOrdering/APPEXTENSION-com.apple.finder.TrimQuickAction | 2 | 3 | Difference |
| finder:pbs:FinderOrdering/is.workflow.actions.image.convert.finder | 4 | 4 | Matches stored value |
| finder:pbs:FinderOrdering/is.workflow.actions.image.removebackground | 5 | 5 | Matches stored value |
| terminal:com.apple.Terminal:Default Window Settings | Nick-Mac | Nick-Mac | Matches stored value |
| terminal:com.apple.Terminal:Startup Window Settings | Nick-Mac | Nick-Mac | Matches stored value |
| terminal:profile:Nick-Mac:BackgroundColor | Encoded appearance data (SHA-256 ba3002439b1a…) | Encoded appearance data (SHA-256 ba3002439b1a…) | Matches stored value |
| terminal:profile:Nick-Mac:Font | Encoded appearance data (SHA-256 86f5b8c8ac9e…) | Encoded appearance data (SHA-256 86f5b8c8ac9e…) | Matches stored value |
| terminal:profile:Nick-Mac:FontAntialias | On | On | Matches stored value |
| terminal:profile:Nick-Mac:FontWidthSpacing | 0.9959677419354839 | 0.9959677419354839 | Matches stored value |
| terminal:profile:Nick-Mac:SelectionColor | Encoded appearance data (SHA-256 22467ac28387…) | Encoded appearance data (SHA-256 22467ac28387…) | Matches stored value |
| terminal:profile:Nick-Mac:TextBoldColor | Encoded appearance data (SHA-256 067e3e8afdd7…) | Encoded appearance data (SHA-256 067e3e8afdd7…) | Matches stored value |
| terminal:profile:Nick-Mac:TextColor | Encoded appearance data (SHA-256 067e3e8afdd7…) | Encoded appearance data (SHA-256 067e3e8afdd7…) | Matches stored value |
| terminal:profile:Nick-Mac:fontAllowsDisableAntialias | 0 | 0 | Matches stored value |
| terminal:profile:Nick-Mac:name | Nick-Mac | Nick-Mac | Matches stored value |
| terminal:profile:Nick-Mac:type | Window Settings | Window Settings | Matches stored value |

### FluidVoice recorded settings — target setup absent

| Stable ID | Recorded | Target result |
| --- | --- | --- |
| voice-transcription:com.FluidApp.app:AudioHistoryBudgetGB | 10.0 | Not present |
| voice-transcription:com.FluidApp.app:AutoUpdateCheckEnabled | Off | Not present |
| voice-transcription:com.FluidApp.app:ContextAwareCapitalizationEnabled | On | Not present |
| voice-transcription:com.FluidApp.app:ContinuousDictationSpacingEnabled | On | Not present |
| voice-transcription:com.FluidApp.app:CopyTranscriptionToClipboard | On | Not present |
| voice-transcription:com.FluidApp.app:CustomDictionaryEntries | {"entries": [{"triggers": ["fluid voice, zieger, merrill, oliva, zimmermann", "fluid voice zieger meryl oliva zimmerman", "fluid voice zieger merrill oliva zimmerman"], "replacement": "FluidVoice, Zegar, Merryl, Oliva, Zimmermann"}]} | Not present |
| voice-transcription:com.FluidApp.app:DictationPromptOff | Off | Not present |
| voice-transcription:com.FluidApp.app:EnableDebugLogs | On | Not present |
| voice-transcription:com.FluidApp.app:EnableStreamingPreview | Off | Not present |
| voice-transcription:com.FluidApp.app:FluidIntelligenceSelectedModelID | fluid-1 | Not present |
| voice-transcription:com.FluidApp.app:LiteralDictationFormattingEnabled | On | Not present |
| voice-transcription:com.FluidApp.app:NotchPresentationMode | minimal | Not present |
| voice-transcription:com.FluidApp.app:OverlayBottomOffset | 50.0 | Not present |
| voice-transcription:com.FluidApp.app:OverlayPosition | top | Not present |
| voice-transcription:com.FluidApp.app:PauseMediaDuringTranscription | On | Not present |
| voice-transcription:com.FluidApp.app:PrivateAIProviderContextTokenLimit | 4096 | Not present |
| voice-transcription:com.FluidApp.app:PromptModeShortcutEnabled | Off | Not present |
| voice-transcription:com.FluidApp.app:SaveAudioWithTranscriptionHistory | On | Not present |
| voice-transcription:com.FluidApp.app:SaveTranscriptionHistory | On | Not present |
| voice-transcription:com.FluidApp.app:SecondaryDictationPromptOff | On | Not present |
| voice-transcription:com.FluidApp.app:SelectedDictationPromptID | __FLUID_1__ | Not present |
| voice-transcription:com.FluidApp.app:SelectedModelByProvider | {"fluid-1": "fluid-1", "custom:fluid-1": "fluid-1"} | Not present |
| voice-transcription:com.FluidApp.app:SelectedProviderID | fluid-1 | Not present |
| voice-transcription:com.FluidApp.app:SelectedSpeechModel | parakeet-tdt | Not present |
| voice-transcription:com.FluidApp.app:ShareAnonymousAnalytics | Off | Not present |
| voice-transcription:com.FluidApp.app:ShowMainWindowAtLoginLaunch | Off | Not present |
| voice-transcription:com.FluidApp.app:TranscriptionSoundVolume | 0.5 | Not present |
| voice-transcription:com.FluidApp.app:TranscriptionStartSound | fluid_sfx_0 | Not present |
| voice-transcription:app:presence | com.FluidApp.app | Not present |
| voice-transcription:asset:vocabulary | {"alpha": 2.8, "minCtcScore": -2.2, "minSimilarity": 0.72, "minCombinedConfidence": 0.64, "minTermLength": 3, "terms": [{"text": "FluidVoice", "aliases": ["fluid voice", "fluid boys"], "weight": 10.0}]} | Not present |
| voice-transcription:control:launch_at_startup | On | Not verifiable while app is absent |
| voice-transcription:control:microphone_selection_mode | manual | Not verifiable while app is absent |
| voice-transcription:control:preferred_input | built-in microphone | Not verifiable while app is absent |
| voice-transcription:control:fallback_input_order_if_present | ["LG UltraFine Display Audio", "Microsoft Teams Audio"] | Not verifiable while app is absent |
| voice-transcription:control:missing_input_policy | Show an available target input in the plan for Nick to choose. | Not verifiable while app is absent |
| voice-transcription:setting:primary_dictation_shortcut | Right Option | Not verifiable while app is absent |
| voice-transcription:setting:activation_mode | toggle | Not verifiable while app is absent |
| voice-transcription:setting:cancel_recording_shortcut | Escape | Not verifiable while app is absent |
| voice-transcription:setting:edit_shortcut | Option+R | Not verifiable while app is absent |
| voice-transcription:setting:edit_shortcut_enabled | On | Not verifiable while app is absent |
| voice-transcription:setting:command_mode_shortcut_enabled | Off | Not verifiable while app is absent |
| voice-transcription:setting:paste_last_shortcut_enabled | Off | Not verifiable while app is absent |
| voice-transcription:setting:text_insertion_mode | clipboard-free insertion | Not verifiable while app is absent |
| voice-transcription:setting:theme | follow system | Not verifiable while app is absent |
| voice-transcription:setting:show_in_dock | On | Not verifiable while app is absent |
| voice-transcription:setting:sound_independent_volume | Off | Not verifiable while app is absent |
| voice-transcription:setting:overlay_preview_characters | 150 | Not verifiable while app is absent |
| voice-transcription:setting:skip_silent_recordings | Off | Not verifiable while app is absent |
| voice-transcription:setting:lowercase_first_letter | Off | Not verifiable while app is absent |
| voice-transcription:setting:remove_trailing_period | Off | Not verifiable while app is absent |
| voice-transcription:setting:notify_ai_failures | On | Not verifiable while app is absent |
| voice-transcription:setting:notify_microphone_changes | On | Not verifiable while app is absent |

### FluidVoice keys with no adopted stored value

These 70 keys have no stored target override. They are review items, not instructions to remove settings. Any overlap with the effective-setting expectations above must be resolved through the app after installation.

`AccentColorOption`, `AppPromptBindings`, `AutoConvertPunctuationEnabled`, `AutomaticDictionaryLearningEnabled`, `BetaReleasesEnabled`, `CancelRecordingHotkeyShortcut`, `CommandModeConfirmBeforeExecute`, `CommandModeHotkeyShortcut`, `CommandModeLinkedToGlobal`, `CommandModeSelectedModel`, `CommandModeSelectedProviderID`, `CommandModeShortcutEnabled`, `ContinuousDictationModeEnabled`, `CustomDictationPrompt`, `DefaultDictationPromptOverride`, `DefaultEditPromptOverride`, `DefaultRewritePromptOverride`, `DefaultWritePromptOverride`, `DictationPromptConfigurations`, `DictationPromptProfiles`, `EditPromptOff`, `EnableAIStreaming`, `EnableTranscriptionSounds`, `FileTranscriptionExpectedSpeakerCount`, `FileTranscriptionSpeakerLabelsEnabled`, `FillerWords`, `FluidIntelligenceBackendPreference`, `GAAVLowercaseFirstLetterEnabled`, `GAAVModeEnabled`, `GAAVRemoveTrailingPeriodEnabled`, `HotkeyMode`, `HotkeyShortcutKey`, `ModelReasoningConfigs`, `NotifyAIProcessingFailures`, `OverlaySize`, `PasteLastTranscriptionHotkeyShortcut`, `PasteLastTranscriptionShortcutEnabled`, `PressAndHoldMode`, `PrimaryDictationShortcuts`, `PrivateAIProviderBoostEnabled`, `PrivateAIProviderPrefixKVCacheEnabled`, `PromptModeHotkeyShortcut`, `PromptModeSelectedPromptID`, `PronunciationMatchingEnabled`, `PunctuationDictionaryPrefix`, `PunctuationDictionaryRules`, `RemoveFillerWordsEnabled`, `RewriteModeHotkeyShortcut`, `RewriteModeLinkedToGlobal`, `RewriteModeSelectedModel`, `RewriteModeSelectedProviderID`, `RewriteModeShortcutEnabled`, `SelectedAppleSpeechLocaleIdentifier`, `SelectedCohereLanguage`, `SelectedEditPromptID`, `SelectedNemotronLanguage`, `SelectedRewritePromptID`, `SelectedWritePromptID`, `SendCustomPromptOnly`, `ShowInDock`, `ShowMicrophoneChangeAlerts`, `ShowThinkingTokens`, `SkipSilentRecordingsEnabled`, `SpokenFormattingActionRules`, `TextInsertionMode`, `ThemePreference`, `TranscriptionPreviewCharLimit`, `TranscriptionSoundIndependentVolume`, `VisualizerNoiseThreshold`, `VocabularyBoostingEnabled`.

### Launch plist inventory

| Plist / scope | Executable evidence | Registration |
| --- | --- | --- |
| /Library/LaunchAgents/com.citrix.ServiceRecords.plist | Executable exists | Not registered under checked label/domain |
| /Library/LaunchAgents/com.google.keystone.xpcservice.plist | Empty dictionary | Not registered under checked label/domain |
| /Library/LaunchAgents/com.adobe.AdobeCreativeCloud.plist | Executable exists | Not registered under checked label/domain |
| /Library/LaunchAgents/com.google.keystone.agent.plist | Empty dictionary | Not registered under checked label/domain |
| /Library/LaunchAgents/com.adobe.ccxprocess.plist | Executable exists | Not registered under checked label/domain |
| /Library/LaunchAgents/us.zoom.updater.login.check.plist | Executable exists | Not registered under checked label/domain |
| /Library/LaunchAgents/com.citrix.safariadapter.plist | Executable exists | state = running; runs = 1; last exit code = (never exited) |
| /Library/LaunchAgents/com.citrix.AuthManager_Mac.plist | Executable exists | state = not running; runs = 0; last exit code = (never exited) |
| /Library/LaunchAgents/us.zoom.updater.plist | Executable exists | Not registered under checked label/domain |
| /Library/LaunchAgents/com.citrix.ReceiverHelper.plist | Executable exists | Not registered under checked label/domain |
| /Library/LaunchAgents/com.microsoft.update.agent.plist | Executable exists | Not registered under checked label/domain |
| /Library/LaunchDaemons/com.google.GoogleUpdater.wake.system.plist | Executable exists | Not registered under checked label/domain |
| /Library/LaunchDaemons/com.citrix.CtxWorkspaceHelperDaemon.plist | Executable exists | state = not running; runs = 0; last exit code = (never exited) |
| /Library/LaunchDaemons/com.citrix.ctxworkspaceupdater.plist | Executable exists | Not registered under checked label/domain |
| /Library/LaunchDaemons/com.google.keystone.daemon.plist | Empty dictionary | Not registered under checked label/domain |
| /Library/LaunchDaemons/com.adobe.acc.installer.v2.plist | Executable exists | Not registered under checked label/domain |
| /Library/LaunchDaemons/com.citrix.ctxusbd.plist | Executable exists | Not registered under checked label/domain |
| /Library/LaunchDaemons/us.zoom.ZoomDaemon.plist | Executable exists | Not registered under checked label/domain |
| /Library/LaunchDaemons/com.microsoft.autoupdate.helper.plist | Executable exists | Not registered under checked label/domain |
| ~/Library/LaunchAgents/com.elgato.StreamDeck.plist | Executable exists | Not registered under checked label/domain |
| ~/Library/LaunchAgents/com.amazon.kpr.ncd.plist | Executable exists | Not registered under checked label/domain |
| ~/Library/LaunchAgents/com.google.keystone.xpcservice.plist | Empty dictionary | Not registered under checked label/domain |
| ~/Library/LaunchAgents/com.dropbox.dropboxmacupdate.xpcservice.plist | Empty dictionary | Not registered under checked label/domain |
| ~/Library/LaunchAgents/com.google.keystone.agent.plist | Empty dictionary | Not registered under checked label/domain |
| ~/Library/LaunchAgents/com.adobe.ccxprocess.plist | Executable exists | Not registered under checked label/domain |
| ~/Library/LaunchAgents/com.nick.tool-cleanup.telemetry-optouts.plist | Executable exists | state = not running; runs = 1; last exit code = 0 |
| ~/Library/LaunchAgents/com.dropbox.DropboxUpdater.wake.plist | Executable exists | state = not running; runs = 29; last exit code = 0 |
| ~/Library/LaunchAgents/com.openai.atlas.update-helper.plist | Missing executable | state = spawn scheduled; runs = 1; last exit code = 78: EX_CONFIG |
| ~/Library/LaunchAgents/com.dropbox.dropboxmacupdate.agent.plist | Empty dictionary | Not registered under checked label/domain |
| ~/Library/LaunchAgents/us.zoom.updater.gui.501.login.check.plist | Missing executable | Not registered under checked label/domain |
| ~/Library/LaunchAgents/com.google.GoogleUpdater.wake.plist | Executable exists | Not registered under checked label/domain |
| ~/Library/LaunchAgents/us.zoom.updater.gui.501.plist | Missing executable | Not registered under checked label/domain |

### Skill installation paths

| Skill | Expected target | Observed discovery entries |
| --- | --- | --- |
| build-employment-opportunity-dossier | ~/.codex/skills/build-employment-opportunity-dossier | ~/.codex/skills/build-employment-opportunity-dossier |
| chinese-poem-workbook | ~/.agents/skills/chinese-poem-workbook | ~/.agents/skills/chinese-poem-workbook |
| email-operations | ~/.codex/skills/email-operations | ~/.codex/skills/email-operations |
| nick-coach | ~/.codex/skills/nick-coach | ~/.codex/skills/nick-coach |
| nick-guided-srs | ~/repos/nick/nick-skills/.agents/skills/nick-guided-srs | ~/repos/nick/nick-skills/.agents/skills/nick-guided-srs |
| nick-mac | ~/repos/nick/nick-skills/.agents/skills/nick-mac | ~/repos/nick/nick-skills/.agents/skills/nick-mac |
| nick-money | ~/.codex/skills/nick-money | None |
| nick-museums | ~/repos/nick/nick-skills/.agents/skills/nick-museums | ~/repos/nick/nick-skills/.agents/skills/nick-museums |
| nick-tool-cleanup | ~/.codex/skills/nick-tool-cleanup | ~/repos/nick/nick-skills/.agents/skills/nick-tool-cleanup; ~/.codex/skills/nick-tool-cleanup |
| test-elementary-knowledge | ~/.codex/skills/test-elementary-knowledge | ~/.codex/skills/test-elementary-knowledge |

</details>
