---
skill_name: email-operations
installation_scope: machine
installation_target: ~/.codex/skills/email-operations
installation_method: symlink
---

# Email Operations Requirements

## Purpose

Apply narrowly authorized, account-specific mailbox housekeeping rules without extending one profile’s authority to another account or action.

## Personal Gmail rule

1. Read the exact mailbox address from `account.local.md` and verify the connected account before making any change.
2. Consider only Inbox messages from `Notify NYC <noreply@everbridge.net>` whose subject identifies them as Notify NYC messages.
3. Archive a candidate when it is more than 48 hours old or conclusively obsolete because the message says the matter ended, was resolved, cancelled, or expired, or because its stated end time passed.
4. Leave a newer message untouched when obsolescence is uncertain.
5. Exhaust every search page and collect the complete candidate set before archiving anything.
6. Archive qualifying individual message IDs by removing only the `INBOX` label; do not use thread-level actions.
7. Preserve every other label and the read/unread state.
8. Search again from the first page after each archive pass. Stop after verification finds no qualifying messages or after three archive-and-verify passes.
9. Report archived and remaining qualifying counts, or report account-verification or operation failure.

## Boundaries

- Do not act when the account profile is absent, ambiguous, or does not match the connected mailbox.
- Do not alter other senders, accounts, or mailbox categories.
- Do not delete, mark read or unread, add labels, forward, reply, draft, send, or unsubscribe.
- Do not claim success while qualifying messages remain.

## Success evidence

- The connected account was verified against exactly one local profile.
- Every candidate page was processed before mutation.
- Verification reports zero qualifying messages, or the run clearly reports failure after the bounded retry limit.
