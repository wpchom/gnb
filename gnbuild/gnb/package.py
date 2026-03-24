#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.dont_write_bytecode = True

from . import utils


def _parser_arguments(parser):
    parser.add_argument("pkgname", metavar="PKGNAME", type=str, help="package name")

    parser.add_argument(
        "-s", "--source", type=str, default=None, help="packages source dir"
    )
    parser.add_argument(
        "-x", "--proxy", type=str, default=os.getenv("GNB_PROXY"), help="download proxy"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", default=False, help="print verbose"
    )

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


def _pkg_package_plat():
    import platform

    plat_sys = platform.uname().system.lower()
    plat_mach = platform.uname().machine.lower()

    # windows, linux, macos
    if plat_sys == "darwin":
        plat_sys = "macos"

    if plat_mach in ["aarch64", "arm64"]:
        plat_mach = "arm64"
    elif plat_mach in ["x86_64", "amd64"]:
        plat_mach = "x86_64"
    elif plat_mach in ["i386", "i686"]:
        plat_mach = "x86"

    return f"{plat_sys}_{plat_mach}"


def _pkg_pkgfile_read(pkgs_dir, pkgname, pkgvers):
    import json

    pkgfile = os.path.join(_pkg_pkgname_path(pkgs_dir, pkgname), "GNBPKG.json")
    if not os.path.exists(pkgfile):
        utils.error(f"Package json [{pkgname}] is not exists")

    try:
        with open(pkgfile) as f:
            pkgjson = json.load(f)
    except Exception as e:
        utils.error(f"Package read [{pkgname}] is not valid: {e}")

    if not "name" in pkgjson or pkgname != pkgjson["name"]:
        utils.error(f"Package name [{pkgname}] is not match")

    if not "versions" in pkgjson or len(pkgjson["versions"]) == 0:
        utils.error(f"Package [{pkgname}] versions is not defined")

    pkgdesc = {"name": pkgname, "version": pkgvers}
    if (pkgvers == None) or (pkgvers == "latest"):
        pkgdesc.update(pkgjson["versions"][0])
    else:
        verlist = []
        for verdesc in pkgjson["versions"]:
            if "url" in verdesc:
                pkgdesc["url"] = verdesc["url"]
            if "path" in verdesc:
                pkgdesc["path"] = verdesc["path"]
            if "version" in verdesc:
                verlist.append(verdesc["version"])
                if verdesc["version"] == pkgvers:
                    pkgdesc["version"] = verdesc["version"]
                    break
        if not "version" in pkgdesc:
            utils.debug(f"Package [{pkgname}] version: {verlist}")
            utils.error(f"Version ({pkgvers}) is not exists")

    pkgplat = _pkg_package_plat()

    if "url" in pkgdesc:
        if type(pkgdesc["url"]) != dict:
            utils.error(f"Package [{pkgname}] url is not a dict")
        if pkgplat in pkgdesc["url"]:
            pkgdesc["url"] = pkgdesc["url"][pkgplat]
        elif "*" in pkgdesc["url"]:
            pkgdesc["url"] = pkgdesc["url"]["*"]
        else:
            utils.error(f"Package [{pkgname}] url of `{pkgplat}` is not defined")

    if "path" in pkgdesc:
        if type(pkgdesc["path"]) != dict:
            utils.error(f"Package [{pkgname}] path is not a dict")
        if pkgplat in pkgdesc["path"]:
            pkgdesc["path"] = pkgdesc["path"][pkgplat]
        elif "*" in pkgdesc["path"]:
            pkgdesc["path"] = pkgdesc["path"]["*"]
        else:
            utils.error(f"Package [{pkgname}] path of `{pkgplat}` is not defined")

    if "type" in pkgjson:
        pkgdesc["type"] = pkgjson["type"]

    return (pkgjson, pkgdesc)


def _pkg_pkgname_path(pkgs_dir, pkgname):
    return os.path.join(pkgs_dir, pkgname[0], pkgname)


def _pkg_pkgtemp_path(pkgs_dir, subdir, pkgname):
    return os.path.join(pkgs_dir, ".tmp", subdir, pkgname[0], pkgname)


def _pkg_download_path(pkgs_dir, pkgdesc):
    download_path = _pkg_pkgtemp_path(pkgs_dir, "download", pkgdesc["name"])

    if ("type" in pkgdesc) and (pkgdesc["type"] in ["binary"]):
        download_path = os.path.join(
            download_path, _pkg_package_plat(), pkgdesc["version"]
        )
    else:
        download_path = os.path.join(download_path, pkgdesc["version"])

    return download_path


def _pkg_resource_path(pkgs_dir, pkgdesc):
    resouce_path = _pkg_pkgtemp_path(pkgs_dir, "resource", pkgdesc["name"])

    if ("type" in pkgdesc) and (pkgdesc["type"] in ["binary"]):
        resouce_path = os.path.join(
            resouce_path, _pkg_package_plat(), pkgdesc["version"]
        )
    else:
        resouce_path = os.path.join(resouce_path, pkgdesc["version"])

    return resouce_path


def _pkg_buildout_path(pkgs_dir, pkgdesc):
    buildout_path = _pkg_pkgtemp_path(pkgs_dir, "buildout", pkgdesc["name"])

    if ("type" in pkgdesc) and (pkgdesc["type"] in ["binary"]):
        buildout_path = os.path.join(
            buildout_path, _pkg_package_plat(), pkgdesc["version"]
        )
    else:
        buildout_path = os.path.join(buildout_path, pkgdesc["version"])

    return buildout_path


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


def _pkg_prepare(args):
    import shutil

    pkgs_dir = args.source
    pkgjson, pkgdesc = _pkg_pkgfile_read(pkgs_dir, args.pkgname, args.version)

    if args.verbose:
        utils.debug("package:", pkgdesc)

    if (not args.clean) and (not args.remove):
        return

    pkgname = pkgdesc["name"]
    pkgvers = pkgdesc["version"]

    if args.build or args.download or args.version != None:
        buildout_path = _pkg_buildout_path(pkgs_dir, pkgdesc)
        resource_path = _pkg_resource_path(pkgs_dir, pkgdesc)

        if os.path.exists(buildout_path) or os.path.exists(resource_path):
            utils.info(f"Package [{pkgname}] clean / remove:")
        else:
            utils.info(f"Package [{pkgname}] nothing exists.")
            return

        if args.clean and os.path.exists(buildout_path):
            utils.debug(f"[-] ({pkgvers}) buildout: {buildout_path}")
            shutil.rmtree(buildout_path)

        if args.remove and os.path.exists(resource_path):
            utils.debug(f"[=] ({pkgvers}) resource: {resource_path}")
            shutil.rmtree(resource_path)

    elif (not args.build) and (not args.download):
        utils.info(f"Package [{pkgname}] clean / remove:")

        nums = 0
        for verdesc in pkgjson["versions"]:
            verdesc["name"] = pkgname
            buildout_path = _pkg_buildout_path(pkgs_dir, verdesc)
            resource_path = _pkg_resource_path(pkgs_dir, verdesc)

            if (args.clean and os.path.exists(buildout_path)) and (
                args.remove and os.path.exists(resource_path)
            ):
                nums += 1
                utils.debug(f"[#] ({pkgvers})")
                shutil.rmtree(buildout_path)
                shutil.rmtree(resource_path)

            elif args.clean and os.path.exists(buildout_path):
                nums += 1
                utils.debug(f"[-] ({pkgvers}) buildout: {buildout_path}")
                shutil.rmtree(buildout_path)

            elif args.remove and os.path.exists(resource_path):
                nums += 1
                utils.debug(f"[=] ({pkgvers}) resource: {resource_path}")
                shutil.rmtree(resource_path)

        if nums == 0:
            utils.debug(f"no version to clean / remove")


def _pkg_download(args):
    # pkg_ver, pkg_path = package_download(
    #     args.pkgname, args.version, args.pkgs_dir, args.proxy, args.remove
    # )

    utils.info(f"Package [{args.pkgname}] download:")
    # utils.debug(f"[+] ({pkg_ver}) in {pkg_path}")


def _pkg_build(args):
    # from . import build

    utils.info(f"Package [{args.pkgname}] build:")
    # utils.debug(f"[*] ({pkg_ver}) in {pkg_path}")


def _pkg_list(args):
    pkgs_dir = args.source
    pkgjson, pkgdesc = _pkg_pkgfile_read(pkgs_dir, args.pkgname, args.version)

    utils.info(f"Package [{args.pkgname}] list:")

    if args.version != None:
        pkgvers = pkgdesc["version"]

        buildout_path = _pkg_buildout_path(pkgs_dir, pkgdesc)
        resource_path = _pkg_resource_path(pkgs_dir, pkgdesc)

        if os.path.exists(buildout_path) and os.path.exists(resource_path):
            utils.debug(f"[*] ({pkgvers}) resource: {resource_path}")
        elif os.path.exists(buildout_path):
            utils.debug(f"[-] ({pkgvers}) resource: {resource_path}")
        elif os.path.exists(resource_path):
            utils.debug(f"[+] ({pkgvers}) resource: {resource_path}")
        else:
            utils.debug(f"[ ] ({pkgvers})")
    else:
        for verdesc in pkgjson["versions"]:
            verdesc["name"] = pkgjson["name"]
            pkgvers = verdesc["version"]

            buildout_path = _pkg_buildout_path(pkgs_dir, verdesc)
            resource_path = _pkg_resource_path(pkgs_dir, verdesc)

            if os.path.exists(buildout_path) and os.path.exists(resource_path):
                utils.debug(f"[*] ({pkgvers}) resource: {resource_path}")
            elif os.path.exists(buildout_path):
                utils.debug(f"[-] ({pkgvers}) resource: {resource_path}")
            elif os.path.exists(resource_path):
                utils.debug(f"[+] ({pkgvers}) resource: {resource_path}")
            else:
                utils.debug(f"[ ] ({pkgvers})")


def action(args):
    if ":" in args.pkgname:
        _pkgname = args.pkgname.split(":")[0]
        args.version = args.pkgname[len(_pkgname) + 1 :]
        args.pkgname = _pkgname
    else:
        args.version = None

    if not args.build and (args.target or args.args):
        utils.error("--target and --args can only be used with --build")

    if args.source == None:
        if os.environ.get("GNB_PKGS_DIR") != None:
            args.source = os.environ.get("GNB_PKGS_DIR")
        else:
            args.source = os.path.join(utils.GNB_REPO_DIR, "packages")

    if args.verbose:
        utils.debug(args)

    _pkg_prepare(args)

    if args.download:
        _pkg_download(args)
    elif args.build:
        _pkg_build(args)
    else:
        _pkg_list(args)


def download(pkgs_dir, pkgname, pkgvers=None, proxy=None, remove=False):
    import shutil
    from . import download

    _, pkgdesc = _pkg_pkgfile_read(pkgs_dir, pkgname, pkgvers)

    download_path = _pkg_download_path(pkgs_dir, pkgdesc)
    resource_path = _pkg_resource_path(pkgs_dir, pkgdesc)

    if remove and os.path.exists(resource_path):
        shutil.rmtree(resource_path)


