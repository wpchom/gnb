#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.dont_write_bytecode = True

import shutil
from . import utils


def _parser_arguments(parser):
    parser.add_argument(
        "pkgname", nargs="?", default=None, help="package name[:version]"
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

    pkgfile = os.path.join(pkgpath(pkgs_dir, pkgname), "GNBPKG.json")
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
    pkgplat = _pkg_package_plat()
    if (pkgvers == None) or (pkgvers == "latest") or (pkgvers == ""):
        pkgdesc = pkgjson["versions"][0]
        pkgdesc["name"] = pkgname
        pkgvers = pkgdesc["version"]
    else:
        verlist = []
        for verdesc in pkgjson["versions"]:
            if "url" in verdesc:
                pkgdesc["url"] = verdesc["url"]
            if "dir" in verdesc:
                pkgdesc["dir"] = verdesc["dir"]
            if "version" in verdesc:
                verlist.append(verdesc["version"])
                if verdesc["version"] == pkgvers:
                    pkgdesc["version"] = verdesc["version"]
                    break

    if not "version" in pkgdesc:
        utils.debug(f"Package [{pkgname}] version: {verlist}")
        utils.error(f"Version ({pkgvers}) is not exists")

    if "url" in pkgdesc:
        if type(pkgdesc["url"]) != dict:
            utils.error(f"Package [{pkgname}] url is not a dict")
        if pkgplat in pkgdesc["url"]:
            pkgdesc["url"] = pkgdesc["url"][pkgplat].format(version=pkgvers)
        elif "*" in pkgdesc["url"]:
            pkgdesc["url"] = pkgdesc["url"]["*"].format(version=pkgvers)
        else:
            utils.error(f"Package [{pkgname}] url of `{pkgplat}` is not defined")

    if "dir" in pkgdesc:
        if type(pkgdesc["dir"]) != dict:
            utils.error(f"Package [{pkgname}] dir is not a dict")
        if pkgplat in pkgdesc["dir"]:
            pkgdesc["dir"] = pkgdesc["dir"][pkgplat].format(version=pkgvers)
        elif "*" in pkgdesc["dir"]:
            pkgdesc["dir"] = pkgdesc["dir"]["*"].format(version=pkgvers)

    if "type" in pkgjson:
        pkgdesc["type"] = pkgjson["type"]

    return (pkgjson, pkgdesc)


def _pkg_pkgtemp_path(pkgs_dir, subdir, pkgname):
    return os.path.join(os.path.expanduser("~"), ".gnbuild", subdir, pkgname[0], pkgname)
    # return os.path.join(pkgs_dir, ".temp", subdir, pkgname[0], pkgname)


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


def _pkg_clean_remove(pkgs_dir, pkgdesc, clean=False, remove=False):
    if (clean == False) and (remove == False):
        return (False, False)

    buildout_dir = _pkg_buildout_path(pkgs_dir, pkgdesc)
    resource_dir = _pkg_resource_path(pkgs_dir, pkgdesc)
    download_tmp = resource_dir + ".tmp"

    if remove and os.path.exists(download_tmp):
        shutil.rmtree(download_tmp)

    download_file = _pkg_check_download(resource_dir, pkgdesc)
    if remove and (download_file != None):
        os.remove(download_file)

    c = False
    r = False
    if os.path.exists(buildout_dir) or os.path.exists(resource_dir):
        if clean and os.path.exists(buildout_dir):
            shutil.rmtree(buildout_dir)
            c = True
        if remove and os.path.exists(resource_dir):
            shutil.rmtree(resource_dir)
            r = True

    return (c, r)


def _pkg_prepare(args):
    pkgjson, pkgdesc = _pkg_pkgfile_read(args.pkgs_dir, args.pkgname, args.version)

    if args.verbose:
        utils.debug("package:", pkgdesc)

    if (not args.clean) and (not args.remove):
        return

    pkgname = pkgdesc["name"]

    if args.build or args.download or (args.version != None):
        pkgvers = pkgdesc["version"]
        c, r = _pkg_clean_remove(args.pkgs_dir, pkgdesc, args.clean, args.remove)
        if (c == False) and (r == False):
            utils.info(f"Package [{pkgname}] nothing exists.")
        else:
            utils.info(f"Package [{pkgname}] clean / remove:")
            if c == True:
                buildout_dir = _pkg_buildout_path(args.pkgs_dir, pkgdesc)
                utils.debug(f"[-] ({pkgvers}) buildout: {buildout_dir}")
            if r == True:
                resource_dir = _pkg_resource_path(args.pkgs_dir, pkgdesc)
                utils.debug(f"[=] ({pkgvers}) resource: {resource_dir}")

    elif (not args.build) and (not args.download):
        utils.info(f"Package [{pkgname}] clean / remove:")
        nums = 0
        for verdesc in pkgjson["versions"]:
            verdesc["name"] = pkgname
            pkgvers = verdesc["version"]
            c, r = _pkg_clean_remove(args.pkgs_dir, verdesc, args.clean, args.remove)
            if c == True:
                buildout_dir = _pkg_buildout_path(args.pkgs_dir, pkgdesc)
                utils.debug(f"[-] ({pkgvers}) buildout: {buildout_dir}")
                nums += 1
            if r == True:
                resource_dir = _pkg_resource_path(args.pkgs_dir, pkgdesc)
                utils.debug(f"[=] ({pkgvers}) resource: {resource_dir}")
                nums += 1

        if nums == 0:
            utils.debug(f"no version to clean / remove")


def _pkg_download(args):
    pkgvers, pkgpath = pkgload(
        args.pkgs_dir, args.pkgname, args.version, args.proxy, args.remove
    )

    utils.info(f"Package [{args.pkgname}] download:")
    utils.debug(f"[+] ({pkgvers}) in {pkgpath}")


def _pkg_build(args):
    from . import build

    _, pkgdesc = _pkg_pkgfile_read(args.pkgs_dir, args.pkgname, args.version)

    pkgname = pkgdesc["name"]
    pkgvers = pkgdesc["version"]

    buildpkg_dir = pkgpath(args.pkgs_dir, pkgname)
    if not os.path.exists(os.path.join(buildpkg_dir, "BUILD.gn")):
        utils.error(f"Package [{pkgname}] does not have BUILD.gn")

    buildout_dir = _pkg_buildout_path(args.pkgs_dir, pkgdesc)
    build_profile = build.get_profile(args.repo_dir, buildpkg_dir, "release")

    # TODO: set package version
    build_args = [f'{pkgname}_pkgver="{pkgvers}"'] + args.args

    build.run_build(
        buildpkg_dir,
        build_profile,
        buildout_dir,
        build_args,
        args.repo_dir,
        args.pkgs_dir,
        args.verbose,
        args.proxy,
        args.target,
    )

    utils.info(f"Package [{args.pkgname}] build:")
    utils.debug(f"[*] ({pkgvers}) build out: {buildout_dir}")


def _pkg_list(args):
    pkgjson, pkgdesc = _pkg_pkgfile_read(args.pkgs_dir, args.pkgname, args.version)

    utils.info(f"Package [{args.pkgname}] list:")

    if args.version != None:
        pkgvers = pkgdesc["version"]

        buildout_dir = _pkg_buildout_path(args.pkgs_dir, pkgdesc)
        resource_dir = _pkg_resource_path(args.pkgs_dir, pkgdesc)

        if os.path.exists(buildout_dir) and os.path.exists(resource_dir):
            utils.debug(f"[*] ({pkgvers}) resource: {resource_dir}")
        elif os.path.exists(buildout_dir):
            utils.debug(f"[-] ({pkgvers}) resource: {resource_dir}")
        elif os.path.exists(resource_dir):
            utils.debug(f"[+] ({pkgvers}) resource: {resource_dir}")
        else:
            utils.debug(f"[ ] ({pkgvers})")
    else:
        for verdesc in pkgjson["versions"]:
            verdesc["name"] = pkgjson["name"]
            pkgvers = verdesc["version"]

            buildout_dir = _pkg_buildout_path(args.pkgs_dir, verdesc)
            resource_dir = _pkg_resource_path(args.pkgs_dir, verdesc)

            if os.path.exists(buildout_dir) and os.path.exists(resource_dir):
                utils.debug(f"[*] ({pkgvers}) resource: {resource_dir}")
            elif os.path.exists(buildout_dir):
                utils.debug(f"[-] ({pkgvers}) resource: {resource_dir}")
            elif os.path.exists(resource_dir):
                utils.debug(f"[+] ({pkgvers}) resource: {resource_dir}")
            else:
                utils.debug(f"[ ] ({pkgvers})")


def _pkg_foreach(args):
    for pkgsub in sorted(os.listdir(args.pkgs_dir)):
        if not os.path.isdir(os.path.join(args.pkgs_dir, pkgsub)):
            continue
        for pkgdef in sorted(os.listdir(os.path.join(args.pkgs_dir, pkgsub))):
            if "GNBPKG.json" in os.listdir(os.path.join(args.pkgs_dir, pkgsub, pkgdef)):
                pkgjson, _ = _pkg_pkgfile_read(args.pkgs_dir, pkgdef, None)

                pkgname = pkgjson["name"]
                verlist = []
                for verinfo in pkgjson["versions"]:
                    pkgvers = verinfo["version"]
                    _, pkgdesc = _pkg_pkgfile_read(args.pkgs_dir, pkgdef, pkgvers)
                    buildout_dir = _pkg_buildout_path(args.pkgs_dir, pkgdesc)
                    resource_dir = _pkg_resource_path(args.pkgs_dir, pkgdesc)

                    if os.path.exists(buildout_dir) and os.path.exists(resource_dir):
                        verlist.append(f"*({pkgvers})")
                    elif os.path.exists(buildout_dir):
                        verlist.append(f"-({pkgvers})")
                    elif os.path.exists(resource_dir):
                        verlist.append(f"+({pkgvers})")
                    else:
                        verlist.append(f"({pkgvers})")

                utils.info(f"Package: {pkgname}")
                utils.debug(f"versions: {', '.join(verlist)}\n")


def action(args):
    if args.pkgname == None:
        args.version = None
    elif ":" in args.pkgname:
        _pkgname = args.pkgname.split(":")[0]
        args.version = args.pkgname[len(_pkgname) + 1 :]
        args.pkgname = _pkgname
    else:
        args.version = None

    if not args.build and (args.target or args.args):
        utils.error("--target and --args can only be used with --build")

    if args.verbose:
        utils.debug(args)

    if (args.download or args.build) and (args.pkgname == None):
        utils.error("pkgname[:version] is required with --download or --build")

    if args.pkgname == None:
        _pkg_foreach(args)
    else:
        _pkg_prepare(args)
        if args.download:
            _pkg_download(args)
        elif args.build:
            _pkg_build(args)
        else:
            _pkg_list(args)


"""
url
curl -o packages/.tmp/resource/x/xxx/(version).tmp/(download_filename).zip
mv .. packages/.tmp/resource/x/xxx/(version).zip

extract
packages/.tmp/resource/x/xxx/(version)/....

git
packages/.tmp/resource/x/xxx/(version)/.git
git clone ... packages/.tmp/resource/x/xxx/(version)
"""

_EXTRACT_EXTENSIONS = [
    ".tar.gz",
    ".tar.bz2",
    ".tar.xz",
    ".zip",
    ".rar",
    ".7z",
    ".tar",
    ".gz",
    ".bz2",
    ".xz",
]


def _pkg_split_extension(filename):
    fname = filename.lower()

    extension = ""

    if fname.endswith((".tar.gz", ".tar.bz2", ".tar.xz")):
        extension = "." + fname.split(".")[-2] + "." + fname.split(".")[-1]
    elif fname.endswith((".zip", ".tar", ".gz", ".bz2", ".xz", ".rar", ".7z")):
        extension = "." + fname.split(".")[-1]
    elif "." in fname:
        parts = fname.split(".")
        if parts[-2] in ["tar", "zip", "rar", "7z"]:
            extension = "." + parts[-2] + "." + parts[-1]
        else:
            extension = "." + parts[-1]
    else:
        extension = "." + os.path.splitext(filename)[-1].lstrip(".")

    return (filename[: -len(extension)], extension)


def _pkg_check_download(resource_dir, pkgdesc):
    checkdir = os.path.dirname(resource_dir)

    if not os.path.exists(checkdir):
        return None

    if ("type" in pkgdesc) and (pkgdesc["type"] in ["binary"]):
        download_name = _pkg_package_plat() + "-" + pkgdesc["version"]
    else:
        download_name = pkgdesc["version"]

    for f in os.listdir(checkdir):
        if not f.startswith(download_name):
            continue
        _, extension = _pkg_split_extension(f)
        if extension in _EXTRACT_EXTENSIONS:
            return os.path.join(checkdir, f)

    return None


def pkgpath(pkgs_dir, pkgname):
    return os.path.join(pkgs_dir, pkgname[0], pkgname)


def pkgload(pkgs_dir, pkgname, pkgvers=None, proxy=None, remove=False):
    from . import download, compress

    _, pkgdesc = _pkg_pkgfile_read(pkgs_dir, pkgname, pkgvers)

    pkgname = pkgdesc["name"]
    pkgvers = pkgdesc["version"]

    resource_dir = _pkg_resource_path(pkgs_dir, pkgdesc)

    if remove and os.path.exists(resource_dir):
        shutil.rmtree(resource_dir)

    pkgurl = pkgdesc["url"]
    if not os.path.exists(resource_dir):
        if pkgurl.endswith(".git"):
            os.makedirs(os.path.dirname(resource_dir), exist_ok=True)
            pkgpath = download.download_by_git(pkgurl, resource_dir, pkgvers, proxy)
        else:
            download_tmp = resource_dir + ".tmp"
            if remove and os.path.exists(download_tmp):
                shutil.rmtree(download_tmp)

            download_file = _pkg_check_download(resource_dir, pkgdesc)
            if remove and (download_file != None):
                os.remove(download_file)
                download_file = None

            if download_file == None:
                pkgpath = download.download_by_url(pkgurl, download_tmp, proxy)
                if pkgpath == None:
                    utils.error(f"Download `{pkgurl}` error")

                _, extension = _pkg_split_extension(pkgpath)
                if not extension in _EXTRACT_EXTENSIONS:
                    utils.error(f"Download `{pkgurl}` not support")

                if ("type" in pkgdesc) and (pkgdesc["type"] in ["binary"]):
                    download_file = os.path.join(
                        os.path.dirname(resource_dir),
                        f"{_pkg_package_plat()}-{pkgvers}{extension}",
                    )
                else:
                    download_file = os.path.join(
                        os.path.dirname(resource_dir), f"{pkgvers}{extension}"
                    )

                shutil.move(pkgpath, download_file)
                shutil.rmtree(download_tmp)

            _, extension = _pkg_split_extension(download_file)
            if extension in _EXTRACT_EXTENSIONS:
                compress.decompress(download_file, resource_dir, True)

    if "dir" in pkgdesc:
        retpath = os.path.abspath(os.path.join(resource_dir, pkgdesc["dir"]))
    else:
        retpath = os.path.abspath(resource_dir)

    return (pkgvers, retpath)
