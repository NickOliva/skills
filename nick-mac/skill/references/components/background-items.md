# Login items and background tasks

The [standard](../../assets/background-items/standard.json) records accepted review policies and known task identities. Every full run includes this component. These are policies to apply to evidence from each target, not a fixed list to install or delete. IDs use `background-items:<item-id>`; record individual task choices with `background-items:task:<scope>:<label>` where needed.

## Inspect and decide

Read `sfltool dumpbtm` and relevant user/system LaunchAgents and LaunchDaemons. Inspect plist contents, executable existence, parent application, user/system scope, and applicable `launchctl print` state. Inspect contents as well as filenames: OneDrive's SyncReporter does not contain OneDrive in its task label. Avoid displaying unrelated environment variables or personal data from service dumps.

Match tasks to intentional installations. A missing executable supports a stale-task finding after checking relocation or alternative installations. Use the target's home directory and numeric user ID; never copy a previous target's UID or absolute home path. Distinguish loaded/scheduled tasks, running processes, and cached UI records. A disabled record referring to Trash is not proof of reinstall. Missing icons and duplicate display names alone do not justify cleanup. If a protected binary cannot be read, report verification as incomplete, not an invalid signature.

Review every standard item and newly found background tasks. For telemetry, inspect the stored opt-out task plus `launchctl getenv ORT_DISABLE_TELEMETRY` and `launchctl getenv POWERSHELL_TELEMETRY_OPTOUT`. A value of `1` proves the login environment setting, not every app's compliance. Do not broaden the opt-out into unrelated settings. Use the readable name in the standard when reporting the custom task; the system may show its executable name, launchctl.

Show observed alternatives and proposed keep/adopt/new/defer choices in the combined alignment plan. Accepted retention policies do not automatically authorize enabling every discovered helper. Cleanup approved on one Mac must be reviewed against the next Mac's actual state.

## Apply and verify

For accepted stale-task removal, unload the exact task in its actual user or system domain before moving its plist to Trash or an agreed backup. An already absent service is not an error; verify whether it is registered first. Do not remove application data, unrelated tasks, or shared Office update/licensing services.

When an app uninstall is approved, account for its updater, launch, and reporting tasks before removing the application. Verify executable absence, launch registration removal, and no remaining related process; inspect installation logs if it reappears. Do not reset the whole macOS background-task database or empty unrelated Trash to clean up a cosmetic record.

For an accepted telemetry-task installation or repair, preserve the exact configuration in the standard, write only its user LaunchAgent, load it in the target login session, and verify the environment value. Do not copy or rename Apple's launchctl executable or create an application solely to alter a Settings label.

Report each policy's actual target result and unresolved checks. The comparison helper lists these items for manual inspection; it does not claim to have inspected their service state.
