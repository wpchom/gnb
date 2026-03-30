set_defaultplat("corss")

target("cmsis", function()
    set_kind("headeronly")

    add_includedirs("CMSIS/Core/Include", { public = true })
    add_headerfiles("CMSIS/Core/Include/(**.h)")
end)
