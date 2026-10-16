# SpecFrame — 自适应提问 · 完整项目需求 · 审查与批准

[English](README.md) · [한국어](README.ko.md) · **简体中文**

![Skill](https://img.shields.io/badge/skill-SpecFrame-2563eb)
![Python](https://img.shields.io/badge/python-3.11%2B-3776ab?logo=python&logoColor=white)
![Runtime](https://img.shields.io/badge/runtime-standard%20library-16a34a)
![Checks](https://github.com/ProjectFrame-skills/SpecFrame/actions/workflows/verify.yml/badge.svg)

## 🚀 安装到 Codex

```bash
git clone https://github.com/ProjectFrame-skills/SpecFrame.git
cd SpecFrame
python3 tools/install_specframe.py
```

需要 Python 3.11+。安装后在新的 Codex 对话中调用 `$specframe`。安装工具还会将只针对对应会话状态的恢复 hook 合并到 Codex 配置；实际执行前，宿主必须信任其准确配置。

**将网站、应用或程序的想法整理为可审查、可批准项目需求的 AI skill。**

SpecFrame 帮助明确**产品服务谁、应该做什么、如何表现，以及怎样判断成功。** 它支持新想法与现有项目改进，依据回答继续提问，重要产品选择由用户决定。

完整范围的需求和最终批准后，可由 [SynFrame](https://github.com/ProjectFrame-skills/SynFrame) 探索实现工具、方法及其组合。

## 主要功能

| 功能 | 作用 |
|---|---|
| 自适应澄清 | 同时提出当前能独立回答的重要问题，再处理剩余不确定事项，不固定问题数量。 |
| 清晰回答框架 | 使用编号和短标签，合并简单输入，分开复杂决策与互斥选项。 |
| 完整范围需求 | 保留目标、范围、约束、角色、流程和排除项，不擅自缩减为 MVP。 |
| 需求工程 | 在输入充分的阶段应用可识别义务、EARS、NASA 质量检查、验收标准和目的失败反例。 |
| 条件式 UI 考虑 | 检查相关网页行为与视觉偏好，不统一强制框架、主题、安装、离线或推送。 |
| 语义保留 | 区分确认事实、建议、证据和待定事项；部分回答只解决实际回答的元素。 |
| 恢复与批准 | 保留当前需求及少量进度指针，在用户确认前审查完整范围。 |

## 安装

辅助工具只使用 Python 标准库，不需要额外 Python 包、专用模型 API key 或推理服务器。判断和工具使用由宿主 AI 完成。

默认位置为 `~/.codex/skills/specframe` 和 `~/.codex/hooks.json`。使用自定义 Codex home 时也可指定路径：

```bash
python3 tools/install_specframe.py \
  --destination /absolute/path/to/skills/specframe \
  --hooks /absolute/path/to/hooks.json
```

安装工具复制实现并保留已有 hook 组。首次更改 hook 前，如已有配置，会保存为 `hooks.json.before-specframe`。它不会改变宿主信任，也不会备份已有 skill 安装；需要旧版本时请另行复制。

其他支持 skills 和本地 Python 执行的宿主可以加载 `skills/specframe/SKILL.md` 及其引用。自动调用 hook 取决于宿主支持；无法自动调用时，应在依赖先前决策的工作之前明确读取恢复状态。

## 使用方法

### 1. 明确新想法

```text
$specframe 我想建立管理定制订单的网站。
我知道现有流程的问题，但还不清楚需要哪些功能和运营规则。
请帮我明确整个项目。
```

**过程：** 目标与环境 → 独立问题 → 将确认回答和待定事项写入当前需求 → 根据回答继续深入。

可以按编号回答、只回答一部分、写“待定”，或请求建议。没有真实案例时，可说明平常流程或预想情境；假设情境与实际事件保持区分。

### 2. 改进现有项目

```text
$specframe 改善这个项目中员工管理变更的方式。
保留现有客户数据和已确认的访问政策。
请检查当前行为，明确需要改变的需求。
```

**过程：** 检查已知功能、数据和政策 → 区分保留与变更 → 明确受影响流程和验收标准。

### 3. 继续已保存工作

```text
$specframe 继续明确当前项目。
在下一轮问题之前，读取已保存需求和剩余决策位置。
```

辅助工具通常会找到项目中的 `.specframe/<CODEX_THREAD_ID>.json`。跨会话继续时，请提供状态路径和原 owner ID。状态存放在项目中，不放在已安装的 skill 内。

这些案例只用于 README，不是运行预设。自动选择取决于宿主，也可明确调用 `$specframe`。

## 工作结构

```text
想法或现有项目
       ↕
自适应提问 ↔ 当前需求与不确定事项
       ↕
全范围审查 → 用户最终批准 → SynFrame → 实现

    上下文丢失 → 读取当前状态 → 继续
```

**宿主 AI** 负责选择问题、理解回答、编写需求和判断质量。**状态辅助工具** 保存和读取宿主写出的判断，执行结构检查与原子写入，不推断产品决策或自动进行语义审查。

当前文档连接来源、目标与独立义务、条件、可观察结果、通过或失败标准、预期或实际证据。没有证据时保持未验证。界面流程以文字描述；设计稿和线框图不属于默认产物。

## 状态与上下文成本

- 保留一份当前需求文档，不另存完整问答。
- 保留条件、例外、责任、排除项和待定事项。
- 仅附带少量焦点、待定位置、下一步和批准状态。
- 合并实质变更；没有变化时不写入。
- 从相关当前段落恢复，不重新搜索整段对话。

质量、恢复和最终审查优先于 token 或时间节省。问题数和文档长度不能证明完整性。整体响应时间、token 节省与用户疲劳受宿主和任务影响，不宣称普遍改善。

## 高级用法

普通用户无需手写状态 JSON。集成时可检查当前需求：

```bash
python3 skills/specframe/scripts/state.py resume
python3 skills/specframe/scripts/state.py index
python3 skills/specframe/scripts/state.py read GOAL SCOPE CONSTRAINTS
python3 skills/specframe/scripts/state.py read --all
```

这些命令使用当前 `CODEX_THREAD_ID`。其他会话或独立进程中，请在子命令**之前**传入相符路径与 owner：

```bash
python3 skills/specframe/scripts/state.py \
  --state /absolute/project/path/.specframe/session-id.json \
  --owner session-id resume
```

[完整运行契约](skills/specframe/references/operating-contract.md)定义责任。[skill 入口](skills/specframe/SKILL.md)说明保存、审查、批准和条件式引用。标志只记录宿主判断，不能证明语义审查或实际用户批准。

## 开发与验证

```bash
python3 -m unittest discover -s tests -v
```

测试覆盖当前状态校验、无变化写入、恢复读取、owner 隔离、hook 过滤、批准失效和标准输入传递。它们不评判提问质量，也不证明真实宿主自动压缩。行为验证应检查实际继续与语义保留，而不只是文件存在。

```text
skills/specframe/             入口、运行契约、引用和辅助工具
tests/                       可复现状态与恢复检查
tools/install_specframe.py   skill 复制及恢复 hook 集成
.github/workflows/verify.yml Python 测试及隔离安装检查
```

本仓库发布实现和使用说明，不含私有协议、个人原始链接、对话全文、项目状态或本地评估历史。SynFrame 和 ProjectFrame 是独立范围，不会一起安装，也不会自动构建产品。

## 常见问题

- **找不到 skill：** 检查安装路径和 `SKILL.md`，在新对话中明确调用。
- **恢复未执行：** 检查宿主支持与 hook 信任。运行 `resume` 后读取相关待定和关联段落，再继续依赖工作。
- **状态缺失、损坏或属于其他会话：** 说明连续性缺口，使用正确路径和 owner。不要虚构先前决策或覆盖其他对话。
- **问题范围过大：** 可要求更小批次。已回答元素应保持解决，再继续剩余重要决策。
- **批准后语义改变：** 文档返回草稿，需重新全范围审查和实际用户确认。

README 采用 [SynFrame 的呈现结构](https://github.com/ProjectFrame-skills/SynFrame)，功能与安装说明依据 SpecFrame 自身实现编写。
