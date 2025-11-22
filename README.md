# GNB

一个用 Python 封装的 GN + Ninja 构建工具，内置轻量包管理与工具链选择。

## 依赖
- `python3`
- `git`（用于包下载）
- `gn`、`ninja`（若系统未安装，将自动按平台下载并使用）

## 快速开始
- 构建示例 `demo_app`：
  ```shell
  python3 gnb.py build -b packages/d/demo_app -p release -t demo_app
  ```
  生成文件位于 `outdir`（默认在当前目录）。

- 更新工具：
  ```shell
  python3 gnb.py update
  ```

## 构建
默认子命令为 `build`，未指定 `target` 时构建所有目标。
```shell
python3 gnb.py [build] [target] [-b <builddir>] [-p <profile>] [-o <outdir>] \
  [--args <kv>] [-c] [-x <proxy>] [-v]
```
执行流程：
```shell
1. gn gen --root=<builddir> --dotfile=<profile> <outdir>
2. ninja -C <outdir> <target>
```
参数说明：
- `-o, --outdir` 输出目录，默认 `./outdir`。
- `-b, --builddir` 构建根目录，默认当前工作目录（需包含 `BUILD.gn`）。
- `-p, --profile` 配置文件，默认 `gnbuild/profiles/debug.gn`；可传文件名或完整路径。
- `-t, --target` 目标名，缺省构建所有目标。
- `--args` 传递 GN 变量（如 `--args profile_toolchain="clang"`）。
- `-c, --clean` 在构建前清理 `outdir`。
- `-x, --proxy` 代理地址（亦可用环境变量 `GNB_PROXY`）。
- `-v, --verbose` 显示详细命令。

说明：生成时自动导出 `compile_commands.json` 以便 IDE 使用。

## 清理
```shell
python3 gnb.py clean <outdir>
```
执行流程：
```shell
1. ninja -C <outdir> -t clean
```

## 包管理
```shell
python3 gnb.py package <pkgname[:version]> [--download|--build|--list] \
  [-c] [-r] [-t <target>] [--args <kv>] [-v] [-x <proxy>]
```
参数说明：
- `pkgname[:version]` 包名与版本，未指定版本则为 `latest`；亦可使用 `-v` 指定版本。
- `-d, --download` 下载包资源。
- `-b, --build` 构建包定义（未下载会先下载）。
- `-l, --list` 列出包版本状态（默认）。
- `-c, --clean` 清理构建输出。
- `-r, --remove` 删除已下载资源。
- `-t, --target` 额外构建目标（仅与 `--build` 一起使用）。
- `--args` 额外 GN 变量（仅与 `--build` 一起使用）。

示例：
```shell
python3 gnb.py package mbedtls --build -t default --args mbedtls_pkgver="latest"
python3 gnb.py package gn --download
python3 gnb.py package ninja --list
```

## 配置与工具链
- Profile 文件：`gnbuild/profiles/debug.gn`、`gnbuild/profiles/release.gn`
- 工具链选择：通过 `profile_toolchain` 控制，支持 `gcc`、`clang`、`arm_none_eabi_gcc`
- 覆盖方式：
  - 在 profile 中修改 `default_args`（如 `profile_toolchain = "clang"`）。
  - 构建时传参：`--args profile_toolchain="clang"`

## 环境变量
- `GNB_PROXY`：网络代理（与 `-x/--proxy` 等效）。
- `GNB_REPO_DIR`：由工具在生成时注入，GN 脚本用于定位仓库路径。

## 目录结构
- `gnbuild/`：构建配置、toolchain、package 模板
- `packages/`：包定义与示例（如 `d/demo_lib`、`d/demo_app`、`m/mbedtls` 等）
- `scripts/`：辅助脚本与 CLI 模块
- `gnb.py`：命令入口

## 代码参考
- 构建入口：`scripts/gnb/build.py` 中 `build_action` 调用 GN/Ninja（scripts/gnb/build.py:97）
- 包管理：`scripts/gnb/package.py` 子命令与版本语法（scripts/gnb/package.py:360）
- Profile 默认与工具链：`gnbuild/profiles/debug.gn`、`gnbuild/toolchain.gni`
