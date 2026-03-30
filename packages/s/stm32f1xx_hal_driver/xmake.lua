package("stm32f1xx_hal_driver", function()
    set_kind("library")

    set_homepage("https://github.com/STMicroelectronics/stm32f1xx-hal-driver")
    set_description("STM32CubeF1 HAL Driver MCU Component")
    set_license("BSD-3-Clause")

    add_urls("https://github.com/STMicroelectronics/stm32f1xx-hal-driver/archive/refs/tags/v$(version).tar.gz",
        { alias = "tarball" })
    add_urls("https://github.com/STMicroelectronics/stm32f1xx-hal-driver/archive/refs/tags/v$(version).zip",
        { alias = "zipball" })

    add_versions("tarball:1.1.10", "dac985f582b763e8a54aee8329fc7cc86e5690d4ed97f48f7bb7a89eb23f94ca")
    add_versions("zipball:1.1.10", "76fe7723907f429e5518ab4a3b40c89a10b065504eb6f20b0f6a5cebe741d3da")

    add_deps("stm32f1xx_device")

    add_configs("confdir", {
        default = nil
    })

    set_policy("package.keep_source", true)
    -- set_policy("package.install_always", true)
    on_install(function(package)
        -- os.cp(path.join(os.scriptdir(), "startup"), "Startup")
        os.cp(path.join(os.scriptdir(), "stm32f1xx_hal_driver.lua"), "xmake.lua")

        local configs = {
            confdir = package:config("confdir")
        }
        local xmake = import("package.tools.xmake")
        xmake.install(package, configs)

        package:add("defines", configs.device)
    end)
end)
