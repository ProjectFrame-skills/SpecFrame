# SpecFrame — Adaptive Questions · Full Project Requirements · Review & Approval

**English** · [한국어](README.ko.md) · [简体中文](README.zh.md)

[![npm](https://img.shields.io/npm/v/specframe-cli?color=cb3837)](https://www.npmjs.com/package/specframe-cli)
![Skill](https://img.shields.io/badge/skill-SpecFrame-2563eb)
![Python](https://img.shields.io/badge/python-3.11%2B-3776ab?logo=python&logoColor=white)
![Runtime](https://img.shields.io/badge/runtime-standard%20library-16a34a)
![Checks](https://github.com/ProjectFrame-skills/SpecFrame/actions/workflows/verify.yml/badge.svg)

## Prerequisites

| Program | When it is required |
|---|---|
| Codex app or CLI | The AI host that runs `$specframe`, with skills, local file access, and permission to execute Python. Installing the npm package alone does not provide an AI host. |
| [Python 3.11+](https://www.python.org/downloads/) | Required for skill installation and the state/recovery helper. SpecFrame uses Python's standard library and does not require a separate database or pip packages. |
| [Node.js 18+](https://nodejs.org/en/download), with npm | Required for the npm installation route and the `specframe` command. Use a currently supported Node.js LTS release. npm is normally included with Node.js. |

**Required:** Codex + Node.js/npm + Python.

Check the required programs before installation:

```bash
node --version
npm --version
python3 --version
```

On Windows, use `python` or `py -3` if that is your Python command. `SPECFRAME_PYTHON` selects an existing Python executable; it does not install Python. Other AI hosts need compatible skill support and local execution. Additional tools or service access depend on the actual goal and are not universal prerequisites.

### Python discovery and installation errors

The npm CLI first uses `python3`/`python` on PATH (`py -3` on Windows). On macOS/Linux, if those cannot run Python 3.11+, it checks Homebrew's standard prefixes and `brew --prefix`, including installed `python@…` formulae. Homebrew is optional; the CLI does not install Python or edit PATH.

`SPECFRAME_PYTHON` explicitly selects one executable. If set, a bad path or version is reported instead of silently selecting another Python. Errors distinguish a missing executable, an old version, permission denial, a failed/timed-out Python check, and an installer failure. An error lists the failed Python checks and the next step.

After installing the global CLI, select a known Python directly if necessary:

```bash
SPECFRAME_PYTHON="/absolute/path/to/python3" specframe install
```

## 🚀 Global installation with npm

```bash
npm install -g specframe-cli@latest
specframe install
```

The first command installs the global CLI; the second installs the actual skill. Check the CLI with `specframe --version`.

Invoke `$specframe` in a new Codex conversation after installation. The installer also merges a thread-scoped recovery hook into Codex configuration; the host must trust its exact definition before it can run.

**An AI skill that turns a website, app, or program idea into a project you can review and approve.**

SpecFrame clarifies **who the product serves, what it should do, how it should behave, and how success will be checked.** It supports new ideas and existing-project changes. Questions adapt to the answers; important product choices remain yours.

After full-scope requirements and your final approval, [SynFrame](https://github.com/ProjectFrame-skills/SynFrame) can explore implementation tools, methods, and their combinations.

## Features

| Capability | What it does |
|---|---|
| Adaptive clarification | Batches important independently answerable questions, then follows remaining uncertainty without a fixed question count. |
| Clear answer templates | Uses numbers and short labels; combines simple inputs and separates complex decisions and incompatible alternatives. |
| Full-scope requirements | Preserves goals, scope, constraints, actors, flows, and exclusions without silently reducing the project to an MVP. |
| Requirements engineering | Applies identifiable obligations, EARS, NASA quality checks, acceptance criteria, and purpose-failure counterexamples when their inputs are available. |
| Conditional UI considerations | Explores relevant web behavior and visual preferences without imposing a framework, theme, installation, offline mode, or push. |
| Meaning preservation | Separates confirmed facts, proposals, evidence, and unknowns; partial answers resolve only the elements actually answered. |
| Recovery and approval | Keeps current requirements and small progress pointers; reviews the whole scope before user confirmation. |

## Installation

The helper uses only Python's standard library. No additional Python package, dedicated model API key, or reasoning server is required. The host AI supplies judgments and tools.

The npm CLI respects `CODEX_HOME`; otherwise it uses `~/.codex`. It installs the skill in `skills/specframe` and merges the recovery hook into `hooks.json` under that home. For explicit paths:

```bash
specframe install \
  --destination /absolute/path/to/skills/specframe \
  --hooks /absolute/path/to/hooks.json
```

The installer copies the implementation and preserves existing hook groups. Before its first hook change, it saves an existing configuration as `hooks.json.before-specframe`. It does not change hook trust or back up an existing skill installation; keep a separate copy if you need the previous version.

Other hosts can load `skills/specframe/SKILL.md` and its references if they support skills and local Python execution. Automatic hook invocation depends on the host. Explicitly read recovery state before dependent work when automatic invocation is unavailable.

## Update

```bash
specframe update
```

Updates the global CLI to the latest published npm version, then runs that version's installer to update the actual skill. Use a new Codex conversation afterward. Keep the same `CODEX_HOME`; if you originally chose explicit paths, pass the same `--destination`, `--hooks` options to `update`. Custom paths are not remembered automatically.

If your older CLI does not recognize `update`, run the two global installation commands above once. If npm succeeds but skill installation fails, fix the reported problem and run `specframe install` with the same path options.

## Usage

### 1. Clarify a new idea

```text
$specframe I want to build a website for managing custom orders.
I know the problems in our current process, but not the features or operating rules.
Help me clarify the full project.
```

**What happens:** goal and environment → independent questions → confirmed answers and unknowns in current requirements → dependent follow-up questions.

Answer by number, give partial answers, say “unknown,” or request a recommendation. Without a real example, describe ordinary workflow or an anticipated situation; hypothetical accounts remain distinct from actual events.

### 2. Improve an existing project

```text
$specframe Improve how staff manage changes in this project.
Keep existing customer data and confirmed access policies.
Inspect current behavior and clarify the required changes.
```

**What happens:** inspect known behavior, data, and policies → distinguish preservation from change → clarify affected flows and acceptance criteria.

### 3. Resume saved work

```text
$specframe Continue clarifying the current project.
Read saved requirements and remaining decision locations before the next questions.
```

The helper normally finds `.specframe/<CODEX_THREAD_ID>.json` in the project. Across sessions, provide the state path and original owner ID. State belongs in your project, outside the installed skill.

These examples are README usage material, not operating presets. Automatic selection depends on the host; explicit `$specframe` invocation is available.

## How it works

```text
Idea or existing project
          ↕
Adaptive questions ↔ Current requirements and uncertainty
          ↕
Whole-scope review → Your final approval → SynFrame → Implementation

          Context loss → Read current state → Continue
```

The **host AI** chooses questions, interprets answers, writes requirements, and judges quality. The **state helper** stores and retrieves host-authored judgments, with structural checks and atomic writes. It does not infer product decisions or perform semantic review.

The current document connects sources and goals to independent obligations, conditions, observable outcomes, pass/fail criteria, and expected or actual evidence. Missing evidence stays unverified. Screen flows are described in text; mockups and wireframes are outside the default deliverable.

## State and context cost

- Keep one current requirements document rather than a separate full Q&A transcript.
- Preserve conditions, exceptions, responsibilities, exclusions, and unknowns.
- Maintain only small focus, pending-location, next-action, and approval pointers.
- Batch meaningful changes; unchanged saves do not write.
- Recover from relevant current sections instead of searching the entire conversation.

Quality, recovery, and final review come before token or time reductions. Counts and document length do not prove completeness. Whole-answer latency, token savings, and user fatigue depend on the host and task; no universal improvement is claimed.

## Advanced usage

Ordinary users need not write state JSON. Integrations can inspect current requirements:

```bash
python3 skills/specframe/scripts/state.py resume
python3 skills/specframe/scripts/state.py index
python3 skills/specframe/scripts/state.py read GOAL SCOPE CONSTRAINTS
python3 skills/specframe/scripts/state.py read --all
```

These commands use the active `CODEX_THREAD_ID`. For another session or a standalone process, pass matching path and owner **before** the subcommand:

```bash
python3 skills/specframe/scripts/state.py \
  --state /absolute/project/path/.specframe/session-id.json \
  --owner session-id resume
```

The [complete operating contract](skills/specframe/references/operating-contract.md) defines responsibilities. The [skill entrypoint](skills/specframe/SKILL.md) covers saving, review, approval, and conditional references. Flags serialize host judgments; they cannot prove semantic review or actual user confirmation.

## Development and validation

```bash
python3 -m unittest discover -s tests -v
npm test
```

Python tests cover current-state validation, no-op writes, recovery reads, owner isolation, hook filtering, approval invalidation, and stdin transport. Node tests cover CLI arguments, isolated installation, hook preservation, and path handling. They do not grade question quality or prove native host compaction. Behavioral checks must inspect actual continuation and preserved meaning, not file existence.

```text
skills/specframe/             Entrypoint, operating contract, references, helper
tests/                       Reproducible state and recovery checks
cli/specframe.mjs            npm command and Python installer bridge
package.json                 npm package metadata and payload allowlist
tools/install_specframe.py   Skill copy and recovery hook integration
.github/workflows/verify.yml Python/Node tests and isolated installation check
```

This repository distributes implementation and usage documentation. Private agreements, personal source links, transcripts, project state, and local evaluation history are excluded. SynFrame and ProjectFrame are separate scopes; they are not bundled and the product is not automatically built.

## Troubleshooting

- **Skill not visible:** Check the installed path and `SKILL.md`, then invoke it in a new conversation.
- **Recovery did not run:** Check host support and hook trust. Run `resume`, then read relevant pending and linked sections before dependent work.
- **State missing, corrupt, or owned by another session:** Report the continuity gap and use the intended path and owner. Do not invent prior decisions or overwrite another conversation.
- **Questions too broad:** Request smaller batches. Answered elements should stay resolved while important remaining decisions continue.
- **Meaning changed after approval:** The document returns to draft and requires whole-scope review and actual user confirmation again.

The README follows [SynFrame's presentation](https://github.com/ProjectFrame-skills/SynFrame); capabilities and installation describe SpecFrame's own implementation.

## Release automation

Main pushes and pull requests run the existing runtime, CLI, package and isolated-install checks with Python3.11/Node18 and Python3.13/Node24. Run **Publish release** manually for a test-and-package preflight; it does not publish.

For a stable release, update `package.json`, commit to `main`, wait for verification, then push a matching `v<version>` tag. The release workflow verifies the tag belongs to `main`, repeats verification, packs the distribution, publishes the exact tarball through npm trusted publishing, and attaches artifacts to a GitHub release. Failed checks stop publishing. A retry skips an already-published npm version only when its integrity matches exactly.

Maintainer setup: register the package's npm trusted publisher for this repository, workflow **publish.yml**, environment **npm**, with direct publishing allowed. The GitHub `npm` environment permits `v*` tags. No long-lived npm publishing token is stored in GitHub. Agensi packages, where present, are built as release assets; marketplace review remains separate.

## Agensi

SpecFrame on Agensi uses live MCP delivery and a separately trusted Codex recovery connection. The optional verified temporary transport reduces helper-source rewriting while preserving complete agreement reloads and current-state ownership. [Setup / 설정 / 配置](https://github.com/ProjectFrame-skills/SpecFrame/blob/main/integrations/agensi/README.md).
