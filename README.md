# GNB

Gn+Ninja Build by Python Module

## Action

### 构建
build为默认缺省逻辑，当未指定target时，默认构建所有目标。
```shell
gnb [build] [-o=outdir] [-b=builddir] [-d=profile] [-t=target]
```
执行步骤：
```shell
1. gn gen --root=<builddir> --dotfile=<profile> <outdir>
2. ninja -C <outdir> <target>
```
参数说明：
- `-o,--outdir` 输出目录，默认值为当前目录下的`outdir`目录。
- `-b,--builddir` 构建目录，默认值为当前目录，并以`BUILD.gn`文件为构建入口。
- `-p,--profile` 配置文件，若非.gn结尾或自动补全，默认值为`GNB`工程中profiles的debug.gn文件。
- `-t,--target` 目标，默认值为空，即构建所有目标。

### 清除
```shell
gnb clean [-o=outdir]
```
执行步骤：
```shell
1. ninja -C <outdir> -t clean
```
参数说明：
- `-o,--outdir` 待清除的目录，默认值为当前目录下的`outdir`目录。

### 包管理
```shell
gnb package <pkgname> [-v=version]
```
参数说明：
- `<pkgname>` 包名，必填项。
- `-c, --clean` 清除包，默认值为False
- `-r, --remove` 删除包，默认值为False

以下参数冲突，只能指定其中一个：
- `-d, --download` 下载包，默认值为False，不携带`-v`下载latest版本，携带`-v`下载指定版本，输出基于该项目的下载路径。
- `-b, --build` 构建包，默认值为False，不携带`-v`默认latest版本，若未下载会先进行下载。
- `-l, --list` 列出包，默认值为True，不携带`-v`默认所有版本， 携带`-v`指定版本。

