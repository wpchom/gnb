#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
from . import utils, download, compress, build

sys.dont_write_bytecode = True


def _parser_arguments(parser):
    parser.add_argument("pkgname", metavar="PKGNAME", type=str, help="package name")
    parser.add_argument("-t", "--version", default=None, help="tag or version")

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-d", "--download", action="store_true", default=False, help="download package"
    )
    group.add_argument(
        "-r", "--remove", action="store_true", default=False, help="remove package"
    )
    group.add_argument(
        "-b", "--build", action="store_true", default=False, help="build package"
    )
    group.add_argument(
        "-c", "--clean", action="store_true", default=False, help="clean package"
    )
    group.add_argument(
        "-l", "--list", action="store_true", default=False, help="list package"
    )


def parser(subparsers):
    parser = subparsers.add_parser("package", aliases=["p"], help="package manager")
    _parser_arguments(parser)


def _pkg_package_path(package_dir, pkgname):
    return os.path.join(package_dir, pkgname[0], pkgname)


def _pkg_download_path(cache_dir, pkg_desc):
    download_path = os.path.join(
        cache_dir, "download", pkg_desc["name"][0], pkg_desc["name"]
    )
    if "platform" in pkg_desc:
        download_path = os.path.join(
            download_path,
            f"{pkg_desc["name"]}_{pkg_desc["platform"]}-{pkg_desc["version"]}",
        )
    else:
        download_path = os.path.join(
            download_path, f"{pkg_desc["name"]}-{pkg_desc["version"]}"
        )

    return download_path


def _pkg_resource_path(cache_dir, pkg_desc):
    resouce_path = os.path.join(
        cache_dir, "resource", pkg_desc["name"][0], pkg_desc["name"]
    )
    if "platform" in pkg_desc:
        resouce_path = os.path.join(
            resouce_path,
            f"{pkg_desc["name"]}_{pkg_desc["platform"]}-{pkg_desc["version"]}",
        )
    else:
        resouce_path = os.path.join(
            resouce_path, f"{pkg_desc["name"]}-{pkg_desc["version"]}"
        )

    return resouce_path


def _pkg_buildout_path(cache_dir, pkg_desc):
    pkgbuild_path = os.path.join(
        cache_dir, "buildout", pkg_desc["name"][0], pkg_desc["name"]
    )
    if "platform" in pkg_desc:
        pkgbuild_path = os.path.join(
            pkgbuild_path,
            f"{pkg_desc["name"]}_{pkg_desc["platform"]}-{pkg_desc["version"]}",
        )
    else:
        pkgbuild_path = os.path.join(
            pkgbuild_path, f"{pkg_desc["name"]}-{pkg_desc["version"]}"
        )

    return pkgbuild_path


def _pkg_get_platform():
    import platform

    plat_sys = platform.uname().system.lower()
    plat_mach = platform.uname().machine.lower()

    if plat_sys == "darwin":
        plat_sys = "macos"
    if plat_sys in ["aarch64", "arm64"]:
        plat_mach = "arm64"
    elif plat_mach in ["x86_64", "amd64"]:
        plat_mach = "x64"
    elif plat_mach in ["i386", "i686"]:
        plat_mach = "x86"

    return (plat_sys, plat_mach)


def _pkg_from_json(package_dir, pkgname, version):
    import json

    pkg_json = {}
    try:
        with open(
            os.path.join(_pkg_package_path(package_dir, pkgname), "GNBPKG.json")
        ) as f:
            pkg_json = json.load(f)
    except Exception:
        utils.error(f"package `{pkgname}` is not exists")

    if not "name" in pkg_json or pkgname != pkg_json["name"]:
        utils.error(f"package `{pkgname}` is not match")

    if not "versions" in pkg_json or len(pkg_json["versions"]) == 0:
        utils.error(f"package `{pkgname}` versions is not defined")

    pkg_desc = {}
    ver_list = []
    if (version == None) or (version == "latest"):
        pkg_desc = pkg_json["versions"][0]
    else:
        for ver_desc in pkg_json["versions"]:
            if "url" in ver_desc:
                pkg_desc["url"] = ver_desc["url"]
            if "dir" in ver_desc:
                pkg_desc["dir"] = ver_desc["dir"]
            if "version" in ver_desc:
                ver_list.append(ver_desc["version"])
                if ver_desc["version"] == version:
                    pkg_desc["version"] = ver_desc["version"]
                    break

    if not "version" in pkg_desc:
        utils.debug(f"package `{pkgname}` version: {ver_list}")
        utils.error(f"package `{pkgname}` version `{version}` is not exists")

    plat_sys, plat_mach = _pkg_get_platform()
    if ("type" in pkg_json) and (pkg_json["type"] in ["binary"]):
        pkg_desc["platform"] = f"{plat_sys}_{plat_mach}"

    if "url" in pkg_desc:
        if type(pkg_desc["url"]) == dict:
            try:
                pkg_desc["url"] = pkg_desc["url"][pkg_desc["platform"]].format(
                    version=pkg_desc["version"]
                )
            except:
                utils.error(
                    f"package `{pkgname}` url of `{pkg_desc["platform"]}` is not defined"
                )
        elif type(pkg_desc["url"]) == str:
            pkg_desc["url"] = pkg_desc["url"].format(version=pkg_desc["version"])
        else:
            utils.error(f"package `{pkgname}` url is invalid")

    if "dir" in pkg_desc:
        if type(pkg_desc["dir"]) == dict:
            try:
                pkg_desc["dir"] = pkg_desc["dir"][pkg_desc["platform"]].format(
                    version=pkg_desc["version"]
                )
            except:
                pkg_desc["dir"] = ""
        elif type(pkg_desc["dir"]) == str:
            pkg_desc["dir"] = pkg_desc["dir"].format(version=pkg_desc["version"])
        else:
            utils.error(f"package `{pkgname}` dir is invalid")

    pkg_desc["name"] = pkgname

    return (pkg_json, pkg_desc)


def package_download(pkgname, version, package_dir, cache_dir, proxy):
    _, pkg_desc = _pkg_from_json(package_dir, pkgname, version)

    download_path = _pkg_download_path(cache_dir, pkg_desc)
    resource_path = _pkg_resource_path(cache_dir, pkg_desc)

    if not os.path.exists(resource_path):
        if pkg_desc["url"].endswith(".git"):
            download_git = download.download_from_git(
                pkg_desc["url"], pkg_desc["version"], download_path, proxy
            )
            os.makedirs(os.path.dirname(resource_path), exist_ok=True)
            os.rename(download_git, resource_path)
        else:
            download_pkg = download.download_from_url(
                pkg_desc["url"], download_path, proxy
            )
            compress.decompress(download_pkg, resource_path, False)
    else:
        # already downloaded
        pass

    return os.path.abspath(os.path.join(resource_path, pkg_desc["dir"]))


def _package_build(args):
    _, pkg_desc = _pkg_from_json(args.pkgs_dir, args.pkgname, args.version)

    pkgdefine_dir = _pkg_package_path(args.pkgs_dir, pkg_desc["name"])
    if not os.path.exists(os.path.join(pkgdefine_dir, "BUILD.gn")):
        utils.error(f"package `{pkg_desc["name"]}` BUILD.gn is not exists")

    buildout_path = _pkg_buildout_path(args.cache_dir, pkg_desc)
    build.build_action(
        pkgdefine_dir,
        os.path.join(args.repo_dir, "dotfiles", "release.gn"),
        buildout_path,
        [f'{pkg_desc["name"]}_pkgver="{pkg_desc["version"]}"'],
        args.repo_dir,
        args.pkgs_dir,
        args.cache_dir,
        args.proxy,
        args.verbose,
    )


"""
package `pkgname`

[+] <version0> (download)
[*] <version1> (download + build)
[-] <version2> (build)
[ ] <version3> (in json)

"""


def _package_json_list(pkg_json, cache_dir, clean=False, remove=False):
    utils.info(f"package `{pkg_json["name"]}`:")

    for ver_desc in pkg_json["versions"]:
        ver_desc["name"] = pkg_json["name"]
        resource_path = _pkg_resource_path(cache_dir, ver_desc)
        buildout_path = _pkg_buildout_path(cache_dir, ver_desc)

        if os.path.exists(buildout_path) and clean:
            shutil.rmtree(buildout_path)
            utils.debug(f"[c] {ver_desc["version"]}")

        elif os.path.exists(resource_path) and remove:
            shutil.rmtree(resource_path)
            utils.debug(f"[r] {ver_desc["version"]}")

        elif os.path.exists(resource_path) and os.path.exists(buildout_path):
            utils.debug(f"[*] {ver_desc["version"]}")
        elif os.path.exists(resource_path):
            utils.debug(f"[+] {ver_desc["version"]}")
        elif os.path.exists(buildout_path):
            utils.debug(f"[-] {ver_desc["version"]}")
        else:
            utils.debug(f"[ ] {ver_desc["version"]}")


def _package_desc_list(pkg_desc, cache_dir, clean=False, remove=False):
    utils.info(f"package `{pkg_desc["name"]}`:")

    resource_path = _pkg_resource_path(cache_dir, pkg_desc)
    buildout_path = _pkg_buildout_path(cache_dir, pkg_desc)

    if clean:
        if os.path.exists(buildout_path):
            shutil.rmtree(buildout_path)
            utils.debug(f"[c] {pkg_desc["version"]} buildout: {buildout_path}")
        else:
            utils.error(f"package `{pkg_desc['name']}-{pkg_desc['version']}` buildout is not exists")

    elif remove:
        if os.path.exists(resource_path):
            shutil.rmtree(resource_path)
            utils.debug(f"[r] {pkg_desc["version"]} buildout: {resource_path}")
        else:
            utils.error(f"package `{pkg_desc["name"]}-{pkg_desc["version"]}` resource is not exists")

    elif os.path.exists(resource_path) and os.path.exists(buildout_path):
        utils.debug(f"[*] {pkg_desc["version"]} resource: {resource_path}")
    elif os.path.exists(resource_path):
        utils.debug(f"[+] {pkg_desc["version"]} resource: {resource_path}")
    elif os.path.exists(buildout_path):
        utils.debug(f"[-] {pkg_desc["version"]} buildout: {buildout_path}")
    else:
        utils.debug(f"[ ] {pkg_desc["version"]}")


def _package_clean(args):
    pkg_json, pkg_desc = _pkg_from_json(args.pkgs_dir, args.pkgname, args.version)

    if args.version == None:
        _package_json_list(pkg_json, args.cache_dir, True, False)
    else:
        _package_desc_list(pkg_desc, args.cache_dir, True, False)


def _package_remove(args):
    pkg_json, pkg_desc = _pkg_from_json(args.pkgs_dir, args.pkgname, args.version)

    if args.version == None:
        _package_json_list(pkg_json, args.cache_dir, False, True)
    else:
        _package_desc_list(pkg_desc, args.cache_dir, False, True)


def _package_list(args):
    pkg_json, pkg_desc = _pkg_from_json(args.pkgs_dir, args.pkgname, args.version)

    if args.version == None:
        _package_json_list(pkg_json, args.cache_dir, False, False)
    else:
        _package_desc_list(pkg_desc, args.cache_dir, False, False)


def module(args):
    if args.list:
        _package_list(args)
    elif args.build:
        _package_build(args)
    elif args.clean:
        _package_clean(args)
    elif args.remove:
        _package_remove(args)
    else:
        pkg_download_path = package_download(
            args.pkgname, args.version, args.pkgs_dir, args.cache_dir, args.proxy
        )
        sys.stdout.write(pkg_download_path)
