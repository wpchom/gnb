# AGENTS.md — mds_repo

嵌入式交叉编译构建系统，基于 GN + Ninja，Python 胶水脚本编排。

## 命令入口

```shell
python3 gnb.py build -b packages/d/demo_app -p release -t demo_app
python3 gnb.py update          # 更新 gn/ninja 工具
python3 gnb.py package <pkg> --build   # 构建外部包
python3 gnb.py clean <outdir>  # ninja clean
```

默认子命令为 `build`；缺省 target 时构建所有目标。

## 架构要点

- `gnb.py` → `gnbuild/scripts/gnb/`（所有 Python 逻辑），`sys.dont_write_bytecode = True` 全局设定。
- `gnbuild/`：GN 构建配置（BUILDCONFIG.gn、toolchain.gni、package.gni）、profiles、toolchains。
- `packages/<首字母>/<包名>/BUILD.gn`：按首字母分目录存放，如 `d/demo_app`、`m/mbedtls`。
- `pkggroup` 模板（package.gni）通过 `exec_script(pkgload.py)` 动态解析包路径，不是静态路径引用。
- GN/Ninja 若系统未安装，`utils.check_gn/check_ninja` 会自动下载到 `~/.gnbuild/`。

## 构建流程与参数

执行顺序：`gn gen` → `ninja -C <outdir>`，脚本一键串联。

- `-p` profile 可传文件名（不带 `.gn` 后缀也行）或完整路径；默认 `debug.gn`。
- `-o` 输出目录默认 `./output/<profile_basename>`（无 .gn 后缀），如 `./output/release`。
- `--args` 传 GN 变量；`gnb_pkgs_dir` 会自动注入，无需手动指定。
- `-c` 构建前先 clean；`-x` 代理（等效 `MDS_GNB_PROXY` 环境变量）。
- `compile_commands.json` 自动导出。

## 关键环境变量

- `MDS_REPO_DIR`：构建时由脚本注入 env，GN 通过 `getenv("MDS_REPO_DIR")` 定位仓库根路径。勿手动覆盖。
- `MDS_GNB_PROXY`：网络代理，与 `-x` 等效。

## 工具链切换

`profile_toolchain` 控制：`gcc`（Linux 默认）、`clang`（macOS 默认）、`arm_none_eabi_gcc` 等。

切换方式：`--args profile_toolchain="clang"` 或在 profile 的 `default_args` 中修改。

## 注意事项

- 无测试、lint、CI 体系，验证方式仅构建成功与否。
- `~/.gnbuild/` 为缓存根（buildout/download/resource），`gnb.py clean` 仅执行 ninja clean，不清缓存。