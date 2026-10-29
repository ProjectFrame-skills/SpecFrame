# SpecFrame on Agensi: Codex setup and recovery

Agensi integration, based on SpecFrame 0.1.4. This integration keeps the original requirements policy and Python state helper. Agensi supplies the skill instructions and references through MCP. A separately installed Codex callback restores the active project connection after compaction; it contains no cached Agensi skill instructions.

## Requirements

- A local Codex host with SessionStart(compact/resume) command hooks, with the exact hook reviewed and trusted. Controlled native recovery was tested on macOS with Codex CLI 0.160.0. The normal CLI hook-review flow was verified; other hosts/operating systems and Desktop hook trust remain unverified.
- Python 3.11+ and shell execution. The Python helper/bridge use only the standard library.
- Read/write access to the chosen persistent project, plus temporary-script execution.
- A signed-in Agensi MCP connection and access to the live SpecFrame listing.

Real Agensi MCP retrieval and Codex automatic compaction recovery were verified on 2026-10-29 in an isolated native CLI host with normally trusted hooks. The public listing was accessible and returned the current skill, operating contract and helper. There is no claim of universal agent compatibility. Automatic recovery remains a required capability; manual resume is not sold as its equivalent.

## 1. Connect Agensi

```sh
codex mcp add agensi --url https://mcp.agensi.io/mcp/auth
codex mcp login agensi
```

If this server is already configured, inspect it instead of adding a duplicate. Complete Agensi's own sign-in flow; never paste account tokens into a chat. Agensi documents one active agent connection per account, so signing in from another agent can disconnect the previous one. A listing still in review may not be loadable through the live catalogue.

## 2. Obtain the independent bridge

The bridge is published separately in this repository's `codex/agensi-recovery-bridge` branch, under `integrations/agensi/`. It is not installed by the Agensi ZIP. Review the two Python files before using them.

On macOS/Linux, download them without executing a remote installer:

```sh
mkdir -p "$HOME/.local/share/specframe-agensi-bridge"
curl --fail --location https://raw.githubusercontent.com/ProjectFrame-skills/SpecFrame/codex/agensi-recovery-bridge/integrations/agensi/bridge.py --output "$HOME/.local/share/specframe-agensi-bridge/bridge.py"
curl --fail --location https://raw.githubusercontent.com/ProjectFrame-skills/SpecFrame/codex/agensi-recovery-bridge/integrations/agensi/bind.py --output "$HOME/.local/share/specframe-agensi-bridge/bind.py"
```

Check `python3 --version`. If Homebrew Python is absent from PATH, inspect `/opt/homebrew/bin/python3` (Apple Silicon) or `/usr/local/bin/python3` (Intel) and use the actual Python 3.11+ executable. Windows requires an equivalent reviewed absolute interpreter/script command; it was not tested in this integration trial.

## 3. Register and trust the callback

Use absolute paths for both Python and bridge.py. Generate a correctly quoted fragment with the interpreter you intend to use:

```sh
python3 - <<'PY'
import json, pathlib, shlex, sys
bridge = pathlib.Path.home() / '.local/share/specframe-agensi-bridge/bridge.py'
print(json.dumps({'hooks': {'SessionStart': [{'matcher': '^(compact|resume)$', 'hooks': [{'type': 'command', 'command': shlex.join([sys.executable, str(bridge)]), 'timeout': 10, 'additionalContextLimit': 0}]}]}}, indent=2))
PY
```

Merge that SessionStart handler into your Codex hooks.json, normally `~/.codex/hooks.json`, alongside existing handlers. Do not replace the file or unrelated hooks. `additionalContextLimit: 0` is paired with this bridge's strict 9,000-byte output cap; it is not advice for unbounded hooks. Review/trust the exact hook through Codex's supported hook review flow (`/hooks` in the CLI). File presence alone does not prove that a trusted callback will run. Do not disable approvals or use the test-only hook-trust bypass as an installation procedure.

## 4. Use SpecFrame

Invoke the actual SpecFrame listing through Agensi and name your project. Its delivery instructions create only a current activation binding under `.specframe/agensi/<session>.json` before the first requirements save. That binding retains the selected listing, MCP server, state location and original owner. It stores no interview transcript, source instructions or change reasons.

During compact/resume, the callback selects only that conversation's binding, validates its state, and instructs Codex to retrieve the full skill and complete operating contract again before dependent work. Relevant unresolved bodies must also be read. A missing/corrupt/wrong-owner bound state stops continuation; unavailable or incomplete MCP delivery must stop dependent requirements work. This behavioral gate is not an enforcement boundary for every possible tool path.

## Verified scope and remaining limits

The real Agensi trial observed native PreCompact(auto), PostCompact(auto), SessionStart(compact), live entrypoint/complete-contract/helper re-fetch and a full current-state read. All 35 current section bodies, owner, decision waiting and draft approval were identical across compaction. This used a narrowed test threshold and inert pressure data, not a manual compact or simulated callback. Earlier local outage and boundary checks are separate evidence; they cover withheld dependent work, ownership, corrupt/missing state, activation order and bounded context. These results do not certify every timeout/version/truncation case, normal Desktop hook trust or other agents.

The package defines requirements, performs quality review and requests actual user approval. It does not implement a product, choose an implementation framework, or bundle SynFrame/ProjectFrame. Current requirements remain in the user's project. No full question log or change-reason history is added.

## Optional verified temporary helper transport

`transport.py` removes the repeated model-authored copy of the helper source. It stages only the actual matching `get_skill` response for `scripts/state.py` when its complete UTF-8 bytes match the independently reviewed SpecFrame 0.1.4 source pin. It has no network client or bundled state-helper copy. The model still authors the current requirements patch, and the unchanged helper still validates and writes it.

Obtain `transport.py` alongside the two bridge files from the separately reviewed `codex/agensi-response-efficiency` branch.

```sh
curl --fail --location https://raw.githubusercontent.com/ProjectFrame-skills/SpecFrame/codex/agensi-response-efficiency/integrations/agensi/transport.py --output "$HOME/.local/share/specframe-agensi-bridge/transport.py"
```
 This is optional; the original temporary-helper execution remains supported. For a reviewed installation, generate additional hook fragments with absolute paths:

```sh
python3 - <<'PY'
import json, pathlib, shlex, sys
script = pathlib.Path.home() / '.local/share/specframe-agensi-bridge/transport.py'
handler = {'type': 'command', 'command': shlex.join([sys.executable, str(script), 'hook']), 'timeout': 1}
hooks = {'PostToolUse': [{'matcher': '^mcp__agensi__get_skill$', 'hooks': [dict(handler, additionalContextLimit=3000)]}]}
for event in ('Stop', 'PreCompact', 'SessionStart', 'Interrupt', 'SessionEnd'):
    hooks[event] = [{'hooks': [dict(handler)]}]
print(json.dumps({'hooks': hooks}, indent=2))
PY
```

Use the actual connected MCP tool name instead of `mcp__agensi__get_skill` if different. Merge these handlers alongside the existing recovery callback and unrelated hooks, then review/trust them through the normal Codex flow. This does not replace the required `SessionStart` recovery bridge. No hook executes downloaded code automatically: a model must explicitly invoke the announced independent runner for the needed state operation.

One pending source lives in a private temporary file until the immediate operation finishes. The runner removes it in `finally`; turn-end, compact, resume, interrupt and session-end handlers remove unused preparations. No preparation is reused after context loss or a user wait. A hard process kill can prevent ordinary cleanup; a leftover is not an instruction cache or approval, and must not be reused. A later matching-session cleanup or explicit removal clears it. Malformed, partial, changed, wrong-server/listing or error responses do not enable the fast path. A different helper version needs independent pin review; it is not silently accepted. Windows and other hosts remain unverified.

## Candidate delivery efficiency

The candidate reuses complete helper source and applicable references only while actually retained. Related reads may share one fresh helper inside a single shell invocation with cleanup in `finally`. The optional transport holds one pending verified delivery only until that operation or a supported cleanup event; it creates no permanent helper installation. After context loss the full entrypoint and complete operating contract are still fetched, and a needed helper is fetched again. Missing or partial delivery still stops dependent work.

Shared source/goal/verification statements may live once in current shared context with explicit references. Each independent obligation keeps its ID, distinct conditions/exceptions, observable pass/fail evidence and any source/status override. Local answers update only affected bodies and pointers. Before saving, reconcile each affected body’s unresolved decisions with the answer. Keep unanswered targets, states and transition directions; shared text consolidation does not resolve a choice. Nonconsecutive question keys use literal labels so display numbering and stored meanings stay aligned. No fixed question count, full interview log or change-reason history is added.

The candidate is not automatically published by these repository changes. To prepare an isolated Agensi package from this unchanged Codex release:

```sh
out=$(mktemp -d /tmp/specframe-agensi-candidate.XXXXXX)
cp -R skills/specframe/. "$out/"
patch -d "$out" -p1 < integrations/agensi/skill.patch
cp integrations/agensi/README.md "$out/references/setup.md"
cp integrations/agensi/package-readme.md "$out/README.md"
```

Use a new empty output folder. The patch must apply cleanly to the selected source; do not bypass failed hunks. The operating contract, domain references, state helper, bridge and Codex/npm release are unchanged. Benchmark results must distinguish the published MCP payload from candidate amendments; an instruction overlay is not evidence that Agensi already serves the candidate.
