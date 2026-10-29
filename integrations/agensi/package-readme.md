# SpecFrame — Agensi candidate

Turn web, app and program ideas into whole-scope requirements through adaptive questions, quality review and actual user approval.

Based on SpecFrame 0.1.4. The operating contract, web/visual references and Python state helper retain their original bytes. The existing Codex/npm release and independent recovery bridge are unchanged. This candidate avoids redundant reads and full-document serialization when current content is retained. Shared-context references remain optional; each obligation and unresolved decision keeps its meaning. It preserves requirements coverage, review and recovery.

## Required setup

Use a local Codex host with a reviewed, trusted SessionStart(compact/resume) hook, Python 3.11+, shell execution, persistent project files, the independent SpecFrame Agensi recovery bridge and a signed-in Agensi MCP connection. The ZIP does not install hooks or change host settings. Automatic recovery remains required; manual resume is not equivalent. See [setup](references/setup.md).

## Delivery and state

Agensi supplies the entrypoint, complete operating contract, applicable references and unchanged helper. Reuse complete source only while actually retained; context loss requires live re-fetch. Execute the helper unchanged from a fresh temporary file, combine related reads in one invocation, and clean up even on failure. The optional independently trusted transport stages the exact pinned MCP helper response for one operation and cleans it after use or supported lifecycle events; it avoids asking the model to rewrite the source. No installed-skill fallback or permanent instruction cache. Keep only current requirements and small activation/progress pointers under .specframe/. No full question transcript or change-reason history. Independent requirement IDs, conditions, exceptions, evidence status and actual user approval boundaries remain intact.

## Validation boundary

Real Agensi delivery and actual Codex CLI 0.160.0 automatic compaction recovery were observed on macOS with normal hook trust on 2026-10-29; all 35 current bodies and decision/approval pointers survived unchanged. The threshold was narrowed for the test. Candidate amendments are separately evaluated against real MCP delivery; they are not claimed to be already published. Desktop, other agents and operating systems are not certified. SynFrame/ProjectFrame are not bundled, and this package does not implement the product.
