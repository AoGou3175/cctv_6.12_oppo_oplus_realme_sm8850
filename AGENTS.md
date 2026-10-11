# CCTV6.12 构建规则

- 沿用外层 `D:/Codex/构建GKI/AGENTS.md` 的安全、快照和验证要求。
- 目标仓库为 `AoGou3175/cctv_6.12_oppo_oplus_realme_sm8850`，上游为 `cctv18/oppo_oplus_realme_sm8850`。
- 同步上游时保留批量 KPM 工作流、`workflow_call`、`inputs.*`、复用输出、`batch_mode` 和含 `SUB_VERSION` 的 ZIP 命名；安全合并，不强制覆盖远程历史。
- 6.12 上游自 2026-10-04 将 `resukisu` 改为 `bakasu`；本项目使用 `bakasu/sukisu/ksunext/ksu/none`，不要把该改名应用到未经核对的 6.1/6.6 项目。
- 当前七个独立版本为 `23/23_gki/23_mtk/38/58/58_mtk/69_gki`；新增版本时同时维护父 job、Release 依赖、成功条件、ZIP 数量和源码说明表格。
- `69_gki` 对应 AOSP GKI 源码 `android16-6.12-2026-03`，不要按其他版本推断机型。
- 管理器下载必须核对真实可用的仓库和资产；2026-10-11 的 `cctv18/BakaSU_CI` 返回 404，当前可用渠道为 `cctv18/ReSukiSU_CI`，后续更新前重新核对。
- KPM 批量入口默认开启 KPM；批量模式只允许父工作流创建统一 Release。
- BakaSU 在 `48fa4bb7ec8bddb8ea932a8c9be0877f89a1fa73` 主动暂停当前 susfs 联合构建；启用 susfs 时固定到此前的 `5b76b884c75f729a220bb317aa4a4fc78f0e0e9c`，关闭 susfs 时仍使用最新 main。后续解除固定前核对上游支持并真实构建验证，不删除上游兼容检查。
- 固定源码后版本号必须按 `git rev-list --count HEAD` 计算，不能继续按 main 计算。
- 静态检查：安装 `tests/requirements.txt`，运行 `python tests/validate_workflows.py <GitHub仓库副本目录>`；另运行 actionlint、汇总 Bash 的 `bash -n` 和 `git diff --check`。
- 静态检查与真实构建结果分开报告；必须基于新提交启动 Actions，并核对七个 ZIP 及最终 Release 资产。
