package("stm32f1xx_device", function()
    set_kind("library")

    set_homepage("https://github.com/STMicroelectronics/cmsis-device-f1")
    set_description("STM32CubeF1 CMSIS Device MCU Component")
    set_license("Apache-2.0")

    add_urls("https://github.com/STMicroelectronics/cmsis-device-f1/archive/refs/tags/v$(version).tar.gz",
        { alias = "tarball" })
    add_urls("https://github.com/STMicroelectronics/cmsis-device-f1/archive/refs/tags/v$(version).zip",
        { alias = "zipball" })

    add_versions("tarball:4.3.5", "2994ffe58af1f819928f11840359565e0293e91dfb840661da77c2e02de24ca3")
    add_versions("zipball:4.3.5", "0561e49540ca8b951b1bec7e9039ccfa056b8c76fc341df586eae3e4b25f28f4")

    add_deps("cmsis", { public = true })

    add_configs("device", {
        default = "STM32F103xB"
    })

    on_load(function(package)
        package:add("defines", package:config("device"))
    end)

    -- set_policy("package.keep_source", true)
    -- set_policy("package.install_always", true)
    on_install(function(package)
        os.cp(path.join(os.scriptdir(), "startup"), "Startup")
        os.cp(path.join(os.scriptdir(), "stm32f1xx_device.lua"), "xmake.lua")

        local configs = {
            device = package:config("device")
        }
        local xmake = import("package.tools.xmake")
        xmake.install(package, configs)
    end)
end)
