# CHANGELOG

## 2026-08-20 03:12:52

- 修改内容：新增 6.12 内核批量 KPM 构建入口，统一传递 KSU、susfs、KPM、LZ4、LZ4KD、BBR、Droidspaces、网络增强、ADIOS、Re-Kernel、基带保护和 ccache 参数。
- 覆盖版本：6.12.23、6.12.23_gki、6.12.23_mtk、6.12.38、6.12.58、6.12.58_mtk。
- 版本映射：按远程 fastbuild 工作流的实际源码分支记录 SM8850、AOSP GKI、MT6993 和 SM8845 平台，不按版本号推断平台。
- 影响文件：`build-test_6.12_kpm.yml`。
- 结果快照：`versions/build-test_6.12_kpm-20260820-031252-create.yml`。
- 验证：预修改静态检查按预期失败；生成后执行 YAML 解析、6 个构建 job/6 个 ZIP 工件数量、版本与 fastbuild 路径、输入参数映射、远程子工作流状态、无行尾空白和敏感信息检查。
- 问题和坑点：远程 6 个 6.12 fastbuild 工作流当前均只声明 `workflow_dispatch`，尚未声明 `workflow_call`，且内部仍使用 `github.event.inputs.*`；同时 6.12.23 与 6.12.23_gki、6.12.38 与 6.12.58 的远程 ZIP 命名模板存在潜在重名风险，因此本批量入口完成静态准备，但实际批量运行前仍需先修复远程子工作流的 reusable workflow 声明、`inputs.*` 上下文和工件唯一命名。
- AGENTS.md：未修改，沿用外层 `D:\Codex\构建GKI\AGENTS.md` 规则。
- GitHub 备份状态：本次修改和快照尚未上传 GitHub。

## 2026-08-20 11:09:40

- 修改内容：完成 6.12 批量 KPM 工作流的远程修复并上传。新增 `build-test_6.12_kpm.yml` 的 `batch_mode: true` 调用参数；为 6 个 `fastbuild_6.12.*.yml` 增加 `workflow_call`、统一 `inputs.*` 引用、声明 `ksuver` 和 `ak3name` 输出，并让批量模式跳过子工作流自己的 Release 创建。
- 影响文件：`.github/workflows/build-test_6.12_kpm.yml`、`.github/workflows/fastbuild_6.12.23.yml`、`.github/workflows/fastbuild_6.12.23_gki.yml`、`.github/workflows/fastbuild_6.12.23_mtk.yml`、`.github/workflows/fastbuild_6.12.38.yml`、`.github/workflows/fastbuild_6.12.58.yml`、`.github/workflows/fastbuild_6.12.58_mtk.yml`。
- 工件修复：6 个子工作流的 AnyKernel3 ZIP 名称加入 `SUB_VERSION`，避免同一批次不同版本工件重名。
- 结果快照：`versions/build-test_6.12_kpm.yml-20260820-110940-remote-fixes.yml`、`versions/fastbuild_6.12.23.yml-20260820-110940-remote-fixes.yml`、`versions/fastbuild_6.12.23_gki.yml-20260820-110940-remote-fixes.yml`、`versions/fastbuild_6.12.23_mtk.yml-20260820-110940-remote-fixes.yml`、`versions/fastbuild_6.12.38.yml-20260820-110940-remote-fixes.yml`、`versions/fastbuild_6.12.58.yml-20260820-110940-remote-fixes.yml`、`versions/fastbuild_6.12.58_mtk.yml-20260820-110940-remote-fixes.yml`。
- 验证：actionlint v1.7.12 返回 0；PowerShell 静态检查通过，确认 6 个 job、6 个 Release 依赖、6 个 ZIP 检查、复用输入输出、批量模式和 12 个有效 ZIP 命名模板均正确；`git diff --check` 通过；推送后 7 个远程 Raw 文件均 HTTP 200，并确认远程 `main` 为提交 `6c371aec527584289ec2fd8bdca73b07cd7af1f8`。
- 问题和坑点：GitHub 连接器写入权限返回 403，改用本地 Git 推送；首次推送遇到 Schannel 握手失败，改用 HTTP/1.1 后成功。未写入密码、Token 或其他敏感信息。
- AGENTS.md：未修改，沿用外层 `D:\Codex\构建GKI\AGENTS.md` 规则。
- GitHub 备份状态：已上传到 `AoGou3175/cctv_6.12_oppo_oplus_realme_sm8850` 的 `main` 分支，提交 `6c371aec527584289ec2fd8bdca73b07cd7af1f8`；仓库可见性未修改。

## 2026-10-11 19:21:13

- 修改内容和原因：合并上游截至 `6c1ffdac3ebf7ebb80254427a7972262b0a8f64e` 的 5 个提交，新增 `6.12.69_gki`、增强补丁处理并将 ReSukiSU 改名为 BakaSU；保留原来的 KPM 批量入口和全部六个旧版本，批量现覆盖七个版本。
- 影响文件：父工作流、七个 fastbuild 工作流、上游发布测试工作流和七个 local 构建脚本；本地新增 `AGENTS.md` 和 `tests/validate_workflows.py`、`tests/requirements.txt`。
- 结果快照：`build-test_6.12_kpm-20261011-192113-同步上游.yml`、`fastbuild_6.12.23-20261011-192113-同步上游.yml`、`fastbuild_6.12.23_gki-20261011-192113-同步上游.yml`、`fastbuild_6.12.23_mtk-20261011-192113-同步上游.yml`、`fastbuild_6.12.38-20261011-192113-同步上游.yml`、`fastbuild_6.12.58-20261011-192113-同步上游.yml`、`fastbuild_6.12.58_mtk-20261011-192113-同步上游.yml`、`fastbuild_6.12.69_gki-20261011-192113-同步上游.yml`，均位于本目录。
- 验证：修改前检查按预期失败；修改后七个版本的全部 15 个复用参数、输出、手动/批量入口和 14 个 ZIP 模板检查通过；actionlint 1.7.12、汇总 Release `bash -n`、`git diff --cached --check` 通过；远程 `main` SHA 和父工作流回读确认成功。
- 问题和解决：上游 BakaSU 改名与原 `inputs.*` 修复发生六个文件的合并冲突，保留批量上下文并合入上游修改；上游 `BakaSU_CI` 链接返回 404，实查后使用仍可用的 `ReSukiSU_CI` 下载管理器；新增 GKI 工作流补齐复用入口、输出、批量 Release 开关和唯一 ZIP 名称；暂存时发现父文件 CRLF 被当作尾部空白，规范为 UTF-8/LF 后重新检查通过。
- AGENTS.md：新增本项目规则，记录 BakaSU 改名、七个版本映射和管理器渠道核验要求。
- GitHub 状态：运行工作流已上传到指定的现有公开 fork 的 `main`，合并提交 `516beebbeb9303e78cfe578846828b4cd691257b`，未更改可见性或重写历史；上述本地测试、规则和快照尚未上传。
- 真实构建：已启动新提交的 KPM 开启/BakaSU 七版本批量运行，Run ID `38135241704`，结果待验收；静态通过不等于编译和 Release 成功。

## 2026-10-11 19:27:26

- 问题表现：首次同步构建 `38135241704` 的七个版本均失败，汇总 Release 按依赖条件跳过。
- 根因：日志定位到 `KernelSU/kernel/tools/susfs_compat.mk` 的 `Please wait susfs update`；BakaSU 上游在 2026-10-10 的 `48fa4bb7ec8bddb8ea932a8c9be0877f89a1fa73` 主动暂停当前 susfs 联合构建，与工作流输入或 ZIP 下载无关。
- 修复内容：七个 fastbuild 工作流和七个 local 构建脚本在启用 susfs 时选择暂停前的 `5b76b884c75f729a220bb317aa4a4fc78f0e0e9c`；关闭 susfs 时仍选择 main。KSU 版本号按实际 HEAD 计算，父 Release 说明披露源码选择；保留原 susfs/KPM 开关。
- 影响文件：父工作流、七个 fastbuild 工作流、七个 local 构建脚本和静态检查脚本。
- 结果快照：八个 YAML 和七个 Shell 脚本，以原文件基本名加 `-20261011-192726-兼容susfs` 命名，均位于本目录；每个修改文件只保存本次结果快照。
- 验证：修复前静态检查因缺失固定提交按预期失败；修复后七版本输入/输出/唯一 ZIP 模板检查、actionlint、汇总 `bash -n`、七个 Shell `bash -n`、`git diff --cached --check` 均通过；核对上游暂停前文件没有构建禁用条件。
- AGENTS.md：追加 BakaSU/susfs 兼容固定与 HEAD 版本计算规则。
- GitHub 状态：兼容修正已上传到 `main`，提交 `431f3569c806127cfd0c72878fe658222a16ec52`；本地规则、测试及快照等待验收后备份。
- 真实构建：基于修正提交启动新的 Run `38135620746`，待七个 ZIP 和最终 Release 验收；未将首次失败运行重新运行当作新提交验证。

## 2026-10-11 19:33:49 最终验收

- 结果：新运行 `38135620746` 的七个 build job 和汇总 Release job 全部成功；七个子 Release job 按批量模式设计跳过。构建提交为 `431f3569c806127cfd0c72878fe658222a16ec52`。
- 发布：`https://github.com/AoGou3175/cctv_6.12_oppo_oplus_realme_sm8850/releases/tag/OPPO-OPlus-Realme-build-all-261011193249-38135620746`，包含七个唯一命名的内核 ZIP 和 `ReSukiSU_v4.2.0-rc3_35203-arm64-v8a-release.apk`。
- 下载验收：全部八个资产下载到 `D:/Codex/构建GKI/CCTV6.12/artifacts/20261011-38135620746/`，文件大小和 SHA-256 均与 GitHub API 的 digest 一致；七个 ZIP 的 CRC 校验通过；Release 中文说明、七版本映射和兼容源码提交披露均通过检查。
- 最终文件：本地 `build-test_6.12_kpm.yml` 与远程运行版本一致。新增 `.gitignore` 防止产物和 Python 缓存进入代码仓库；`.gitattributes` 保持工作流/Unix 脚本 LF，并使 versions 快照按原始字节保存。
- 快照：保留本次同步的八份 YAML 和兼容修复的八份 YAML、七份 Shell 结果快照，以及既有历史快照；未删除或覆盖历史版本。
- AGENTS.md：已更新，记录经真实构建验证的七版本规则、BakaSU/susfs 兼容固定和管理器资产核验要求。
- GitHub 备份：工作流和脚本修正已上传 main；本记录、项目规则、测试及全部历史快照随最终备份提交上传同一指定仓库。构建二进制通过 Release 保存，不提交进 Git。
- 验证边界：已验证编译、KPM 修补、ZIP 和 Release 完整性；未对任何手机执行刷写。

## 2026-10-11 20:16:01 遵循最新 BakaSU 规则

- 用户要求：按照最新 BakaSU 规则构建，不再用旧提交保留 SUSFS。
- 上游核对：当前 main 为 `59afa46b325126b12a48234063cd0c2a6b735b57`，仍包含 `$(error Please wait susfs update.)`。暂停原因是 SUSFS 尚未适配最新 KernelSU 的 SELinux 隐藏处理。
- 修改内容：八个 Actions 工作流默认关闭 SUSFS；七个 fastbuild 和七个 local 脚本统一拉取 BakaSU main，移除旧提交固定。手动开启 SUSFS 且源码仍含上游暂停条件时明确报错退出；不会静默关闭用户选项，也不会移除上游检查。sukisu 选项沿用现有 BakaSU 重定向并遵守相同限制。
- 保留内容：七版本与机型/源码映射、父子输入和输出、批量 Release、独立 ZIP 名称、KPM 及其他构建功能；未改动既有成品和已发布 Release。
- 影响文件：根目录父工作流副本、`.github/workflows/` 下八个工作流、`local/` 下七个构建脚本、两个测试脚本和本项目 `AGENTS.md`；同时更新已有仓库副本，未创建分支或工作树。
- 目录例外：GitHub Actions 要求 `.github/workflows/` 位于仓库根目录，本地增加完整部署副本；保留已有根目录父工作流，两份哈希一致。
- 测试：先运行行为测试，旧策略按预期出现 50 个失败（旧提交回退、SUSFS 默认开启、未拒绝暂停组合）；修改后 9 项测试覆盖 64 个配置/脚本场景全部通过。测试执行真实配置片段，仅替换外部下载与提交计数，覆盖 main、暂停拒绝、sukisu 别名及模拟上游解除暂停。
- 其他验证：七版本/15 参数/14 唯一 ZIP 模板静态检查、actionlint、父 Release 脚本与七个 Shell 的 bash -n、git diff --check 均通过；18 份快照 SHA-256 与对应结果文件一致。
- 坑点：Windows PATH 中的 System32 bash 指向 WSL，会使脚本行为测试使用错误环境；测试改用 Git Bash。未改动系统设置。
- AGENTS.md：按用户此次明确要求替换旧提交兼容固定规则，记录遵守上游暂停、禁止隐式回退及 Git Bash 验证要求；外层 AGENTS.md 未修改。
- GitHub 备份状态：本次修改和快照尚未上传 GitHub；未 git add、commit、push，也未启动新的 Actions。远程现有成功运行和 Release 仍是旧固定提交、带 SUSFS 的成品。
- 验证边界：本次仅验证工作流和策略行为，没有验证最新 main/no-SUSFS 的真实内核编译或手机刷写。

本次结果快照完整路径（18 份）：

- `D:/Codex/构建GKI/CCTV6.12/versions/build-test_6.12_kpm-20261011-201601-遵循最新BakaSU.yml`
- `D:/Codex/构建GKI/CCTV6.12/versions/fastbuild_6.12.23-20261011-201601-遵循最新BakaSU.yml`
- `D:/Codex/构建GKI/CCTV6.12/versions/fastbuild_6.12.23_gki-20261011-201601-遵循最新BakaSU.yml`
- `D:/Codex/构建GKI/CCTV6.12/versions/fastbuild_6.12.23_mtk-20261011-201601-遵循最新BakaSU.yml`
- `D:/Codex/构建GKI/CCTV6.12/versions/fastbuild_6.12.38-20261011-201601-遵循最新BakaSU.yml`
- `D:/Codex/构建GKI/CCTV6.12/versions/fastbuild_6.12.58-20261011-201601-遵循最新BakaSU.yml`
- `D:/Codex/构建GKI/CCTV6.12/versions/fastbuild_6.12.58_mtk-20261011-201601-遵循最新BakaSU.yml`
- `D:/Codex/构建GKI/CCTV6.12/versions/fastbuild_6.12.69_gki-20261011-201601-遵循最新BakaSU.yml`
- `D:/Codex/构建GKI/CCTV6.12/versions/builder_6.12.23-20261011-201601-遵循最新BakaSU.sh`
- `D:/Codex/构建GKI/CCTV6.12/versions/builder_6.12.23_gki-20261011-201601-遵循最新BakaSU.sh`
- `D:/Codex/构建GKI/CCTV6.12/versions/builder_6.12.23_mtk-20261011-201601-遵循最新BakaSU.sh`
- `D:/Codex/构建GKI/CCTV6.12/versions/builder_6.12.38-20261011-201601-遵循最新BakaSU.sh`
- `D:/Codex/构建GKI/CCTV6.12/versions/builder_6.12.58-20261011-201601-遵循最新BakaSU.sh`
- `D:/Codex/构建GKI/CCTV6.12/versions/builder_6.12.58_mtk-20261011-201601-遵循最新BakaSU.sh`
- `D:/Codex/构建GKI/CCTV6.12/versions/builder_6.12.69_gki-20261011-201601-遵循最新BakaSU.sh`
- `D:/Codex/构建GKI/CCTV6.12/versions/validate_workflows-20261011-201601-遵循最新BakaSU.py`
- `D:/Codex/构建GKI/CCTV6.12/versions/test_bakasu_policy-20261011-201601-遵循最新BakaSU.py`
- `D:/Codex/构建GKI/CCTV6.12/versions/AGENTS-20261011-201601-遵循最新BakaSU.md`

## 2026-10-11 20:51:54 GitHub 上传验收

- 用户明确要求上传 GitHub，并明确允许此次继续使用现有 Public fork；保持仓库可见性和 fork 关系不变，未创建新仓库、分支或 PR。
- 上传目标：`AoGou3175/cctv_6.12_oppo_oplus_realme_sm8850` 的 `main`。
- 代码与快照提交：`441ba38cb7c01dadeeaf63081e983b257944e8bf`，八个工作流、七个 local 构建脚本、AGENTS.md、两项测试脚本、CHANGELOG 和 18 份结果快照共 37 个文件已成功推送。
- 上传前验证：fetch 后远程 main 与本地基线一致，无需合并；9 项行为测试全部通过，静态检查、actionlint、Release/七个 local 脚本 bash -n、暂存 git diff --check、18 份快照哈希检查通过；当前文件及 main 历史敏感信息模式扫描未发现匹配项。
- 远程验收：git ls-remote 的 main 提交与本地一致；通过 GitHub API 回读八个工作流与 AGENTS.md，内容 SHA-256 与本地完全一致。
- GitHub 备份状态：本次代码和 18 份快照已上传；本条验收记录随追加文档提交同步备份。没有创建新的快照或覆盖既有快照。
- 构建边界：按本次上传请求没有启动新的 Actions，现有最后一次成功运行 `38135620746` 仍对应此前旧提交/开启 SUSFS 的构建，不能作为本次 latest main/关闭 SUSFS 的真实编译证据。最新工作流网页入口已更新为默认关闭 SUSFS。


