---
name: email-operations
description: Apply explicitly authorized, account-specific email housekeeping rules. Use for scheduled or user-requested mailbox operations that name an existing account profile; never apply one account's rules to another account.
---

# Email Operations

Apply exactly one named account profile per run.

Before changing email, verify that the connected mailbox is the exact account named by the profile. If the account cannot be verified, stop without changing anything. Perform only the actions authorized by that profile; do not infer additional cleanup rules.

## Personal Gmail

Account: read the exact mailbox address from `account.local.md`. If the local profile is missing or does not name exactly one account, stop without changing any mailbox.

Authorized rule:

- Consider only messages from `Notify NYC` that are currently in the Inbox.
- Archive a considered message when either:
  - its received timestamp is more than 48 hours before the current run; or
  - it is conclusively obsolete because the message explicitly says the matter is resolved, cancelled, expired, or ended, or because a stated event or end time has passed.
- If obsolescence is unclear, leave the message in the Inbox unless it is more than 48 hours old.

Use this exhaustive procedure for every run:

1. Search the Inbox for messages whose sender is `Notify NYC <noreply@everbridge.net>` and whose subject identifies them as Notify NYC messages. Request the maximum supported page size and follow every `next_page_token` until there are no more pages. Collect the complete candidate set before changing any message; do not archive while paginating.
2. Use each candidate's received timestamp to apply the 48-hour rule exactly. Read the content of candidates that are not yet 48 hours old only when needed to decide whether they are conclusively obsolete.
3. Archive qualifying messages by removing only the `INBOX` label from their individual Gmail message IDs. Process all qualifying IDs in supported batches; do not use a thread-level archive action.
4. Run the same exhaustive search again from the first page. Verify that no remaining candidate is more than 48 hours old or conclusively obsolete. If any qualifying messages remain, archive those individual messages and verify again, for at most three archive-and-verify passes total.
5. Do not report success unless verification finds zero qualifying messages remaining. If qualifying messages remain after three passes, report failure and the remaining count.

For this profile, archive means remove the Inbox label while preserving the message, its other labels, and its read/unread state.

Do not alter messages from any other sender or any other account. Do not delete, mark read or unread, label, forward, draft, reply, send, unsubscribe, or perform any other email action.

After the run, report the number of messages archived and the number of qualifying messages remaining after verification. If the mailbox could not be verified or the operation failed, report that instead of claiming success.
