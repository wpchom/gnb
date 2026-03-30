set_defaultplat("corss")

add_requires("cmsis")

option("device", function()
    set_default("STM32F103xB")
end)

target("stm32f1xx_device", function()
    set_kind("static")

    add_options("device")

    add_packages("cmsis", { pbulic = true })
    add_includedirs("Include", { public = true })

    add_headerfiles("Include/(**.h)")
    add_files("Source/Templates/system_stm32f1xx.c")

    on_load(function(target)
        target:add("defines", get_config("device"), { public = true })
        target:add("files", path.join("Startup", "startup_" .. string.lower(get_config("device")) .. ".c"))
    end)
end)
