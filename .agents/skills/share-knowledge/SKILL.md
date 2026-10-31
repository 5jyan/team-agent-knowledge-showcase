---
name: share-knowledge
description: Use when asked to propose, update, or retire evidence-backed shared team knowledge through a GitHub pull request. Reads current canonical knowledge and runs validation; never publishes to Hindsight or merges the proposal.
---

# Share knowledge through a reviewed Git change

Use this skill only for a durable finding that another engineer or agent could
apply. A conversation summary, an untested guess, or a private preference is
not team knowledge. The configuration example is intentionally narrow. Always
check the current Git record rather than treating examples as the latest truth.

The Git repository is the source of truth. Hindsight may provide useful
context, but its Team Bank and any personal memory that came from team
knowledge are hints only. Do not treat a recalled page as approval, a current
revision, or proof that a rule still applies.

## Safety and authority boundaries

- Never place passwords, API keys, access tokens, private keys, session
  cookies, customer data, confidential documents, unredacted logs, or other
  secrets in a candidate. Stop and ask for a redacted, shareable description
  when evidence contains them.
- Never call a Hindsight `retain`, `remember`, `ingest`, or equivalent write
  operation for the Team Bank from this skill. The Publisher is the only
  component that may update the Team Bank, and it runs after a human merges
  approved YAML on `main`.
- Never approve, merge, or self-approve the pull request. The user is the
  reviewer and merge authority. A draft PR is a proposal, not a published
  rule.
- Do not claim that GitHub branch protection, Hindsight ACLs, or automatic
  synchronization exist unless the target repository explicitly proves them.
  This prototype assumes a trusted local user and documents those limits.
- Do not silently broaden a rule. Applicability, limitations, source revision,
  and evidence must travel with the candidate.

## 1. Resolve and inspect the canonical repository

Find the knowledge repository before editing anything. Use this order:

1. `TEAM_KNOWLEDGE_REPO`, when it is set.
2. This repository root, when it contains `knowledge/` and `schemas/`.
3. A path or URL supplied by the user.

If none is available, stop with the exact missing input. Do not create a local
replacement with a guessed schema.

Read the target repository's `README`, contribution instructions, schema,
examples, validator, and existing knowledge before drafting. Search for the
exact identifier and related terms. Follow the repository's current paths and
field names; this plugin deliberately does not freeze a template contract.
If a schema or validator is absent, report that gap instead of presenting an
unvalidated YAML file as ready to publish.

For the demo repository, the evidence lives under
`examples/config-validation/`. Re-run the documented tests and demo before
making claims about `COMP-015`:

```bash
python3 -m unittest discover -s examples/config-validation -p 'test_*.py' -v
python3 examples/config-validation/run_demo.py
```

Record the reviewed source commit and the exact commands/results. Do not claim performance improvements that the
toy demo does not measure.

## 2. Classify the observation and collect evidence

Convert the current work into one small candidate. For a bugfix, capture:

- a stable knowledge identifier (reuse the canonical identifier when updating
  an existing rule);
- the observed problem and the user-visible or test-visible failure;
- the proposed behavior and the exact applicability conditions;
- known limitations and cases where the agent must abstain;
- source repository, commit/revision, relevant file or test path, and commands
  that reproduce the evidence;
- the proposing author and the candidate lifecycle state required by the
  repository's schema.

Use the repository's schema names and status vocabulary. In the current
`team-agent-knowledge` contract, a record is a `bugfix` with a stable
`COMP-NNN` id, `status: active|retired`, structured `problem`/`cause`/
`solution`, explicit `limitations` and `scope`, reproducible `evidence`,
`maintenance`, and `references`. The current schema has no `proposed` status:
the draft PR state is the proposal, and an `active` record becomes canonical
only after the user merges it. If the target contract changes, read it and
follow the new vocabulary. If a field is not defined, prefer leaving it out
and explaining the omission over inventing an unreviewed convention. Keep the
patch focused on one finding; split unrelated observations into separate
proposals.

Before writing, scan candidate text, generated files, and copied test output
for secret-like values. Replace them with a safe description and a stable
public reference. Never include an entire environment dump or an unredacted
stack trace when a short excerpt is enough.

## 3. Compare with existing canonical knowledge

Search the knowledge repository itself, not only Hindsight. For each possible
match, read the complete record and compare:

- identifier and current lifecycle status;
- revision/version and source commit;
- applicability and exclusions;
- evidence links and last verification;
- whether the candidate is a new rule, an update, or a deprecation.

Prefer an update to the same identifier when the rule's meaning is changing.
Do not create a duplicate just because a recalled memory has a different title.
If the current canonical record is newer or the evidence conflicts, show the
conflict and ask the user whether to prepare a superseding proposal.

If Hindsight is available, recall is read-only context. Label every fact that
came from it as a hint and verify it against the current Git source before it
enters the candidate. The skill has no permission to write team memory.

## 4. Draft, validate, and show the change

Create a branch with a descriptive, local name such as
`agent/knowledge/comp-015-update`. Put the candidate in the path required by the
target repository (the current contract uses `knowledge/<id>.yaml`). The
current record may use `status: active` when it is a proposed replacement, but
it is not canonical until the user merges the PR; use `retired` only when the
record is genuinely withdrawn and its evidence is preserved.

Run all repository-provided checks, including the schema validator and relevant
demo tests. For the current repository, the local check is
`python3 scripts/validate.py knowledge` (and `--verify-remote` only when the
user explicitly wants remote evidence checked). At minimum run `git diff
--check` and the commands documented by the target README. Review the rendered
diff for:

- complete provenance and reproducible evidence;
- explicit scope and limitations;
- no secret or confidential content;
- no accidental changes outside the knowledge candidate and required metadata.

If checks fail, fix the candidate or report the failure. Do not bypass the
validator or mark a failing check as passing.

## 5. Open a draft PR for human review

After local validation, create a draft pull request against the repository's
default branch. The PR body must state:

1. what was observed and why it is reusable;
2. the source commit, tests, and other evidence;
3. applicability and explicit exclusions;
4. whether this is a new record, an update, or a deprecation;
5. checks run and any remaining gaps;
6. that the Team Bank is unchanged until a human merges and the Publisher
   processes the approved `main` revision.

Use GitHub tools or `gh pr create --draft` when the user's request authorizes
pushing the branch and creating the PR. Do not print, inspect, or copy any
credential. If `gh` is missing or unauthenticated, leave the validated branch
and patch in place and provide the exact command for the user to run; do not
pretend that a PR was opened.

Finish by reporting the branch, PR URL (if created), files changed, checks and
their results, and remaining risks. The user must inspect the diff and decide
whether to approve and merge it.

## Guidance for an agent consuming team knowledge (B)

When a Team Bank result or personal memory derived from team knowledge appears,
use it only as a lead. Before applying the rule, fetch the latest approved Git
source and verify the record's identifier, status, revision/version, source
commit, applicability, and exclusions. Confirm that the current task matches
the recorded scope and rerun or inspect the cited evidence when practical.

Abstain from applying the recalled rule when the source record cannot be found,
the status is not the contract's active/approved state, the revision is stale
or ambiguous, the evidence is missing, or the task falls outside the recorded
scope. (The current prototype uses `status: active`; a later contract may name
the equivalent approved state differently.) Say what could not be verified and
proceed with a safe independent solution or ask the user. If an old personal
memory conflicts with current Git, current Git wins; do not silently reuse the
old claim.

When the rule is used, cite the knowledge identifier, source revision, and
evidence in the work result. A later correction must update the Git record via a
new reviewed PR; this skill does not directly repair the Team Bank.
