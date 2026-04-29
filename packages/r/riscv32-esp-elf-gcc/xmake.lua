package("riscv32-esp-elf-gcc", function()
    set_kind("toolchain")
    set_homepage("https://github.com/espressif/crosstool-NG")
    set_description("espressif riscv32 gcc")

    if (os.host() == "linux") then
        if (os.arch() == "x86_64") then
            set_urls(
                "https://github.com/espressif/crosstool-NG/releases/download/esp-$(version)/riscv32-esp-elf-$(version)-x86_64-linux-gnu.tar.xz"
            )
            add_versions("15.2.0_20251204", "ace5aae6afe98f754947be043d40173e2e22ace57754b11a394b7238eefa01cf")
        elseif (os.arch() == "arm64") then
            set_urls(
                "https://github.com/espressif/crosstool-NG/releases/download/esp-$(version)/riscv32-esp-elf-$(version)-aarch64-linux-gnu.tar.xz"
            )
            add_versions("15.2.0_20251204", "90cccb3ef035f016836dd7c292528b27333a716d42b9361a68005d178c0f70bf")
        end
    elseif (os.host() == "macosx") then
        if (os.arch() == "x86_64") then
            set_urls(
                "https://github.com/espressif/crosstool-NG/releases/download/esp-$(version)/riscv32-esp-elf-$(version)-x86_64-apple-darwin.tar.xz"
            )
            add_versions("15.2.0_20251204", "6d4709eadf4c66aecb51c0ff9c7b068eefa6ecec37aa7817f172c9f735318e73")
        elseif (os.arch() == "arm64") then
            set_urls(
                "https://github.com/espressif/crosstool-NG/releases/download/esp-$(version)/riscv32-esp-elf-$(version)-aarch64-apple-darwin.tar.xz"
            )
            add_versions("15.2.0_20251204", "0869d1083532c631808543dd802885f02dbe1bb3bd640be0dee827e82ded768d")
        end
    elseif (os.host() == "windows") then
        if (os.arch() == "x86_64") then
            set_urls(
                "https://github.com/espressif/crosstool-NG/releases/download/esp-$(version)/riscv32-esp-elf-$(version)-x86_64-w64-mingw32.zip"
            )
            add_versions("15.2.0_20251204", "c61488aa15f49146aae918267110f775a52c3cef3844cbf261f475ef97523c3d")
        elseif (os.arch() == "i386") then
            set_urls(
                "https://github.com/espressif/crosstool-NG/releases/download/esp-$(version)/riscv32-esp-elf-$(version)-i686-w64-mingw32.zip"
            )
            add_versions("15.2.0_20251204", "a52d9c855f1771527d2a6b6a6012ddff3f17bb5c937830b163aa8418177c86da")
        end
    end

    on_install("@windows", "@linux", "@macosx", function(package)
        os.vcp("*", package:installdir())
    end)

    on_test(function(package)
        local gcc = "riscv32-esp-elf-gcc"
        if gcc and is_host("windows") then
            gcc = gcc .. ".exe"
        end
        os.vrunv(gcc, { "--version" })
    end)
end)
