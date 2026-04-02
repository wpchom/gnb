package("cmsis", function()
    set_kind("library", { headeronly = true })

    set_homepage("https://github.com/ARM-software/CMSIS_6")
    set_description("CMSIS Version 6")
    set_license("Apache-2.0")

    add_urls("https://github.com/ARM-software/CMSIS_6/archive/refs/tags/v$(version).tar.gz", { alias = "tarball" })
    add_urls("https://github.com/ARM-software/CMSIS_6/archive/refs/tags/v$(version).zip", { alias = "zipball" })

    add_versions("tarball:6.3.0", "331df74000876b8fb07933658cbf402c4d9f831b429258792d2c34ab5a6c5bf7")
    add_versions("tarball:6.2.0", "35a6bbb89c6b8afe616861b4a8f640f385b6510ff977aeb056e1fd4cb9930529")
    add_versions("tarball:6.1.0", "d8a044e4b50b7112476d6855a12c729ae2b70b3f77a2a038c23890e9a3515973")

    add_versions("zipball:6.3.0", "e09a9d795c5064a8c9bf64245d72bc4a03c54907d485bc02fa75c09fb4b808ce")

    set_policy("package.keep_source", true)
    -- set_policy("package.install_locally", true)
    on_install(function(package)
        os.cp(path.join(os.scriptdir(), "cmsis.lua"), "xmake.lua")

        local xmake = import("package.tools.xmake")
        xmake.install(package)
    end)
end)
