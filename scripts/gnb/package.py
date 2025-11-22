#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.dont_write_bytecode = True

from . import utils


def _parser_arguments(parser):
    parser.add_argument("pkgname", metavar="PKGNAME", type=str, help="package name")

    parser.add_argument(
        "-c", "--clean", action="store_true", default=False, help="clean package"
    )
    parser.add_argument(
        "-r", "--remove", action="store_true", default=False, help="remove package"
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-d", "--download", action="store_true", default=False, help="download package"
    )
    group.add_argument(
        "-b", "--build", action="store_true", default=False, help="build package"
    )
    group.add_argument(
        "-l", "--list", action="store_true", default=True, help="list package"
    )

    parser.add_argument(
        "-t", "--target", default=None, help="additional build target, with --build"
    )
    parser.add_argument(
        "--args",
        action="append",
        default=[],
        help="additional build arguments, with --build",
    )


def parser(subparsers):
    parser = subparsers.add_parser("package", aliases=["p"], help="package manager")
    _parser_arguments(parser)


def _pkg_package_path(pkgs_dir, pkgname):
    return os.path.join(pkgs_dir, pkgname[0], pkgname)


def _pkg_download_path(pkgs_dir, pkg_desc):
    download_path = os.path.join(
        pkgs_dir, ".tmp/download", pkg_desc["name"][0], pkg_desc["name"]
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


def _pkg_resource_path(pkgs_dir, pkg_desc):
    resouce_path = os.path.join(
        pkgs_dir, ".tmp/resource", pkg_desc["name"][0], pkg_desc["name"]
    )
    if "platform" in pkg_desc:
        resouce_path = os.path.join(
            resouce_path,
            f"{pkg_desc["platform"]}-{pkg_desc["version"]}",
        )
    else:
        resouce_path = os.path.join(resouce_path, f"{pkg_desc["version"]}")

    return resouce_path


def _pkg_buildout_path(pkgs_dir, pkg_desc):
    pkgbuild_path = os.path.join(
        pkgs_dir, ".tmp/buildout", pkg_desc["name"][0], pkg_desc["name"]
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
    if plat_mach in ["aarch64", "arm64"]:
        plat_mach = "arm64"
    elif plat_mach in ["x86_64", "amd64"]:
        plat_mach = "x86_64"
    elif plat_mach in ["i386", "i686"]:
        plat_mach = "x86"

    return (plat_sys, plat_mach)


def _pkg_from_json(pkgs_dir, pkgname, version):
    import json

    pkg_json = {}
    try:
        with open(
            os.path.join(_pkg_package_path(pkgs_dir, pkgname), "GNBPKG.json")
        ) as f:
            pkg_json = json.load(f)
    except Exception:
        utils.error(f"Package [{pkgname}] is not exists")

    if not "name" in pkg_json or pkgname != pkg_json["name"]:
        utils.error(f"Package [{pkgname}] is not match")

    if not "versions" in pkg_json or len(pkg_json["versions"]) == 0:
        utils.error(f"Package [{pkgname}] versions is not defined")

    pkg_desc = {}
    ver_list = []
    if (version == None) or (version == "latest"):
        # if not match the version url/dir, use the last version
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
        utils.debug(f"Package [{pkgname}] version: {ver_list}")
        utils.error(f"Version ({version}) is not exists")

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
                    f"Package [{pkgname}] url of `{pkg_desc["platform"]}` is not defined"
                )
        elif type(pkg_desc["url"]) == str:
            pkg_desc["url"] = pkg_desc["url"].format(version=pkg_desc["version"])
        else:
            utils.error(f"Package [{pkgname}] url is invalid")

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
            utils.error(f"Package [{pkgname}] dir is invalid")

    pkg_desc["name"] = pkgname

    return (pkg_json, pkg_desc)


def _pkg_build(args):
    from . import build

    _, pkg_desc = _pkg_from_json(args.pkgs_dir, args.pkgname, args.version)

    pkgdefine_dir = _pkg_package_path(args.pkgs_dir, pkg_desc["name"])
    if not os.path.exists(os.path.join(pkgdefine_dir, "BUILD.gn")):
        utils.error(f"Package [{pkg_desc["name"]}] BUILD.gn is not exists")

    buildout_path = _pkg_buildout_path(args.pkgs_dir, pkg_desc)
    build_profile = build.get_profile(args.repo_dir, pkgdefine_dir, "release")

    build_args = [f'{pkg_desc["name"]}_pkgver="{pkg_desc["version"]}"'] + args.args

    build.build_action(
        pkgdefine_dir,
        build_profile,
        buildout_path,
        build_args,
        args.repo_dir,
        args.pkgs_dir,
        args.proxy,
        args.verbose,
        args.target if ("target" in args) and (args.target != "") else "default",
    )


def package_download(pkgname, version, pkgs_dir, proxy=None, remove=False):
    from . import download, compress

    _, pkg_desc = _pkg_from_json(pkgs_dir, pkgname, version)

    download_path = _pkg_download_path(pkgs_dir, pkg_desc)
    resource_path = _pkg_resource_path(pkgs_dir, pkg_desc)

    if not os.path.exists(resource_path):
        if pkg_desc["url"].endswith(".git"):
            download_git = download.download_from_git(
                pkg_desc["url"], pkg_desc["version"], download_path, proxy
            )
            os.makedirs(os.path.dirname(resource_path), exist_ok=True)
            os.rename(download_git, resource_path)
        else:
            download_pkg = download.download_from_url(
                pkg_desc["url"], download_path, proxy, remove
            )
            compress.decompress(download_pkg, resource_path, False)
    else:
        # already downloaded
        pass

    return pkg_desc["version"], os.path.abspath(
        os.path.join(resource_path, pkg_desc["dir"])
    )


def _pkg_download(args):
    pkg_ver, pkg_path = package_download(
        args.pkgname, args.version, args.pkgs_dir, args.proxy, args.remove
    )

    utils.info(f"Package [{args.pkgname}] download:")
    utils.debug(f"[+] ({pkg_ver}) in {pkg_path}")


"""
Package [pkgname] clean / remove :
[-] (<version>) [clean]
[=] (<version>) [remove]
[#] (<version>) [clean + remove]

Package [pkgname] download:
[+] (<version>) in <path>

Package [pkgname] list:
[*] (<version>) [download + build]
[+] (<version>) [download]
[-] (<version>) [build]
[ ] (<version>) [descript]

"""


def _pkg_pre_action(args):
    import shutil

    pkg_json, pkg_desc = _pkg_from_json(args.pkgs_dir, args.pkgname, args.version)

    if (not args.clean) and (not args.remove):
        return

    if args.build or args.download or args.version != None:
        buildout_path = _pkg_buildout_path(args.pkgs_dir, pkg_desc)
        resource_path = _pkg_resource_path(args.pkgs_dir, pkg_desc)

        if os.path.exists(buildout_path) or os.path.exists(resource_path):
            utils.info(f"Package [{pkg_json["name"]}] clean / remove:")
        else:
            utils.info(f"Package [{pkg_json["name"]}] nothing exists.")
            return

        if args.clean and os.path.exists(buildout_path):
            utils.debug(f"[-] ({pkg_desc['version']}) buildout: {buildout_path}")
            shutil.rmtree(buildout_path)

        if args.remove and os.path.exists(resource_path):
            utils.debug(f"[=] ({pkg_desc['version']}) resource: {resource_path}")
            shutil.rmtree(resource_path)

    elif (not args.build) and (not args.download):
        utils.info(f"Package [{pkg_json["name"]}] clean / remove:")

        nums = 0
        for ver_desc in pkg_json["versions"]:
            ver_desc["name"] = pkg_json["name"]
            buildout_path = _pkg_buildout_path(args.pkgs_dir, ver_desc)
            resource_path = _pkg_resource_path(args.pkgs_dir, ver_desc)

            if (args.clean and os.path.exists(buildout_path)) and (
                args.remove and os.path.exists(resource_path)
            ):
                nums += 1
                utils.debug(f"[#] ({pkg_desc['version']})")
                shutil.rmtree(buildout_path)
                shutil.rmtree(resource_path)

            elif args.clean and os.path.exists(buildout_path):
                nums += 1
                utils.debug(f"[-] ({pkg_desc['version']}) buildout: {buildout_path}")
                shutil.rmtree(buildout_path)

            elif args.remove and os.path.exists(resource_path):
                nums += 1
                utils.debug(f"[=] ({pkg_desc['version']}) resource: {resource_path}")
                shutil.rmtree(resource_path)

        if nums == 0:
            utils.debug(f"no version to clean / remove")


def _pkg_list(args):
    pkg_json, pkg_desc = _pkg_from_json(args.pkgs_dir, args.pkgname, args.version)

    utils.info(f"Package [{args.pkgname}] list:")

    if args.version != None:
        buildout_path = _pkg_buildout_path(args.pkgs_dir, pkg_desc)
        resource_path = _pkg_resource_path(args.pkgs_dir, pkg_desc)
        if os.path.exists(buildout_path) and os.path.exists(resource_path):
            utils.debug(f"[*] ({pkg_desc['version']}) resource: {resource_path}")
        elif os.path.exists(buildout_path):
            utils.debug(f"[-] ({pkg_desc['version']}) resource: {resource_path}")
        elif os.path.exists(resource_path):
            utils.debug(f"[+] ({pkg_desc['version']}) resource: {resource_path}")
        else:
            utils.debug(f"[ ] ({pkg_desc['version']})")
    else:
        for ver_desc in pkg_json["versions"]:
            ver_desc["name"] = pkg_json["name"]
            buildout_path = _pkg_buildout_path(args.pkgs_dir, ver_desc)
            resource_path = _pkg_resource_path(args.pkgs_dir, ver_desc)
            if os.path.exists(buildout_path) and os.path.exists(resource_path):
                utils.debug(f"[*] ({ver_desc['version']}) resource: {resource_path}")
            elif os.path.exists(buildout_path):
                utils.debug(f"[-] ({ver_desc['version']}) resource: {resource_path}")
            elif os.path.exists(resource_path):
                utils.debug(f"[+] ({ver_desc['version']}) resource: {resource_path}")
            else:
                utils.debug(f"[ ] ({ver_desc['version']})")


def action(args):
    if ":" in args.pkgname:
        _pkgname = args.pkgname.split(":")[0]
        args.version = args.pkgname[len(_pkgname) + 1 :]
        args.pkgname = _pkgname
    else:
        args.version = "latest"

    if not args.build and (args.target or args.args):
        utils.error("--target and --args can only be used with --build")

    _pkg_pre_action(args)
    if args.download:
        _pkg_download(args)
    elif args.build:
        _pkg_build(args)
    else:
        _pkg_list(args)
