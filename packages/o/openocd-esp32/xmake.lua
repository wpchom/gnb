package("openocd-esp32", function()
    set_kind("binary")
    set_homepage("https://github.com/espressif/openocd-esp32")
    set_description("espressif riscv32 gdb")

    if (os.host() == "linux") then
        if (os.arch() == "x86_64") then
            set_urls(
                "https://github.com/espressif/openocd-esp32/releases/download/v$(version)/openocd-esp32-linux-amd64-$(version).tar.gz"
            )
            add_versions("0.12.0-esp32-20260304", "dbd7ecf751431c70628176fbf1ce404c3ff28027e91b66bda7f834a2d5ff5b81")
        elseif (os.arch() == "arm64") then
            set_urls(
                "https://github.com/espressif/openocd-esp32/releases/download/v$(version)/openocd-esp32-linux-arm64-$(version).tar.gz"
            )
            add_versions("0.12.0-esp32-20260304", "7fbe82e36f8e34a7a3118045fd7888754afbfe4c60cfaee0ac70663fd5965f63")
        end
    elseif (os.host() == "macosx") then
        if (os.arch() == "x86_64") then
            set_urls(
                "https://github.com/espressif/openocd-esp32/releases/download/v$(version)/openocd-esp32-macos-$(version).tar.gz"
            )
            add_versions("0.12.0-esp32-20260304", "be6951d9766f88fad11060314f6c3469c56715a60f2715aaeb7d806afc935c0d")
        elseif (os.arch() == "arm64") then
            set_urls(
                "https://github.com/espressif/openocd-esp32/releases/download/v$(version)/openocd-esp32-macos-arm64-$(version).tar.gz"
            )
            add_versions("0.12.0-esp32-20260304", "a36099d3a47241e816693d9bd719198e4667ad67f0a027404d90584d44b6842d")
        end
    elseif (os.host() == "windows") then
        if (os.arch() == "x86_64") then
            set_urls(
                "https://github.com/espressif/openocd-esp32/releases/download/v$(version)/openocd-esp32-win64-$(version).zip"
            )
            add_versions("0.12.0-esp32-20260304", "ad29bd55f2b7ad39669fbeeec32012954359dcfc0ecfa5a03068589b4d0e8613")
        elseif (os.arch() == "i386") then
            set_urls(
                "https://github.com/espressif/openocd-esp32/releases/download/v$(version)/openocd-esp32-win32-$(version).zip"
            )
            add_versions("0.12.0-esp32-20260304", "a9db16887fb0df26d1c3e495203c9edcd86d9262b2be7b7d929f8017194add31")
        end
    end

    on_install("@windows", "@linux", "@macosx", function(package)
        os.vcp("*", package:installdir())
    end)

    on_test(function(package)
        local openocd = "openocd"
        if openocd and is_host("windows") then
            openocd = openocd .. ".exe"
        end
        os.vrunv(openocd, { "--version" })
    end)
end)
