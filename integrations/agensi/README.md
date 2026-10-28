# SpecFrame on Agensi: Codex setup and recovery

Agensi review build, based on SpecFrame 0.1.4. This integration keeps the original requirements policy and Python state helper. Agensi supplies the skill instructions and references through MCP. A separately installed Codex callback restores the active project connection after compaction; it contains no cached Agensi skill instructions.

## Requirements

- A local Codex host with SessionStart(compact/resume) command hooks, with the exact hook reviewed and trusted. Controlled native recovery was tested on macOS with Codex CLI 0.160.0. Other hosts/operating systems and the normal Desktop trust flow are not verified by those tests.
- Python 3.11+ and shell execution. The Python helper/bridge use only the standard library.
- Read/write access to the chosen persistent project, plus temporary-script execution.
- A signed-in Agensi MCP connection and access to the live SpecFrame listing.

This is an Agensi review integration. The actual Agensi-hosted delivery is not yet verified end to end. Local controlled delivery and actual Codex automatic compaction were tested separately from marketplace approval. There is no claim of universal agent compatibility. Automatic recovery remains a required capability; manual resume is not sold as its equivalent.

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

Local MCP stand-in tests observed real automatic compaction, callback execution, instruction re-fetch, preservation of confirmed conditions/exceptions and unresolved decisions, planned-versus-executed verification, draft approval, and unchanged current state. An outage trial withheld product answers and approval inference. Boundary tests cover ownership, corrupt/missing state, activation order and bounded context. These do not certify actual Agensi delivery, every timeout/version/truncation case, normal Desktop hook trust, or other agents.

The package defines requirements, performs quality review and requests actual user approval. It does not implement a product, choose an implementation framework, or bundle SynFrame/ProjectFrame. Current requirements remain in the user's project. No full question log or change-reason history is added.
