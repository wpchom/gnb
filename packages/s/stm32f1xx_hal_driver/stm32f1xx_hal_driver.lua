set_defaultplat("corss")

add_requires("stm32f1xx_device")

option("confdir", function()
    set_default(nil)
end)

target("stm32f1xx_hal_driver", function()
    set_kind("static")

    add_options("confdir")

    add_packages("stm32f1xx_device", {public = true})
    add_includedirs("Inc", { public = true })

    add_headerfiles("Inc/(**.h)")
    add_files("Src/*.c|*_template.c")

    on_load(function(target)
        if get_config("confdir") then
            target:add("includedirs", get_config("confdir"), { public = true })
        end
    end)
end)
