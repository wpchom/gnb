add_requires("cmsis", { system = false })

option("device", function()
    set_default("STM32F103xB")
end)

target("stm32f1xx_device", function()
    set_kind("static")

    add_packages("cmsis")

    add_options("device")
    add_includedirs("Include", { public = true })

    add_headerfiles("Include/(**.h)")
    add_files("Source/Templates/system_stm32f1xx.c")

    on_load(function(target)
        target:add("files", path.join("Startup", "startup_" .. string.lower(get_config("device")) .. ".c"))
        target:add("defines", get_config("device"), { public = true })
    end)
end)
