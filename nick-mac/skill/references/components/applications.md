# Applications

Component: `applications`. The [application manifest](../../assets/applications/standard.json) records Nick's reviewed inclusion choices by application identity. Software versions are out of scope.

## Inspect and review

Check identity and presence by bundle ID, including system and user application locations. The comparison helper checks common locations; inspect other installation locations if a required app appears absent. Do not assume a missing bundle means an app is unavailable without checking alternatives.

Use `applications:app:<bundle-id>` for inclusion decisions and `applications:configuration:<bundle-id>` for configuration review. Required presence and chosen settings are separate items. Additional application configurations await review; inspect portable settings, show their current values, and let Nick adopt or revise them. Do not label an installed application fully aligned when its configuration remains undefined. FluidVoice settings are covered by the voice transcription component.

`not-required` permits either presence or absence. It never requests removal. `pending` leaves inclusion undecided and produces no installation/removal action. Keynote, Numbers, Slack, and OneDrive are not required. Other discovered tools remain candidates until reviewed.

Elgato Stream Deck and its Corsair background helper are also optional (`not-required`). Nick explicitly selects the target computers; neither monitor connection nor installation on another target makes them required. Keep computer selections in individual run history, not a named-machine list in portable artifacts. Retention does not itself authorize changing the background-startup switch.

## Apply accepted choices

Include proposed installations and configuration changes in the combined alignment plan. Accepted inclusion does not authorize installation during an inspection. For a missing required application, identify its official vendor or App Store source, licensing or sign-in needs, and any consequential permissions before acceptance. Use the normal supported installer without release pins or version alignment. Built-in applications may require a different availability check; do not replace system apps blindly.

Record chosen portable configuration values and their inspection/application procedure as Nick defines them. Each differing setting uses keep-recorded, adopt-observed, define-new, or defer. Preserve unrelated settings and exclude credentials, account tokens, and private content. Do not interpret this manifest as authorization to remove any application.

## Verify

Recheck required identities and each approved configuration change. Report missing applications, blocked installations, and settings awaiting review separately. Independent application updates do not produce alignment differences.
