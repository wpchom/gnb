package("riscv32-esp-elf-gdb", function()
    set_kind("binary")
    set_homepage("https://github.com/espressif/binutils-gdb")
    set_description("espressif riscv32 gdb")

    if (os.host() == "linux") then
        if (os.arch() == "x86_64") then
            set_urls(
                "https://github.com/espressif/binutils-gdb/releases/download/esp-gdb-v$(version)/riscv32-esp-elf-gdb-$(version)-x86_64-linux-gnu.tar.gz"
            )
            add_versions("16.3_20250913", "4e3cf8b7d11c7a2d1b50f40b1c50c0671dfe7eb13782c27c8a8cfdc8548bcdd4")
        elseif (os.arch() == "arm64") then
            set_urls(
                "https://github.com/espressif/binutils-gdb/releases/download/esp-gdb-v$(version)/riscv32-esp-elf-gdb-$(version)-aarch64-linux-gnu.tar.gz"
            )
            add_versions("16.3_20250913", "8f1f4f24fa534c76ed9d71efffbf728cc30169e911742d7bd67dd0fdcf5f3ae3")
        end
    elseif (os.host() == "macosx") then
        if (os.arch() == "x86_64") then
            set_urls(
                "https://github.com/espressif/binutils-gdb/releases/download/esp-gdb-v$(version)/riscv32-esp-elf-gdb-$(version)-x86_64-apple-darwin24.5.tar.gz"
            )
            add_versions("16.3_20250913", "2d5e5efead0b189e13cfe2670ca9d6d5965378ef3632d0b163a14f2f0536c274")
        elseif (os.arch() == "arm64") then
            set_urls(
                "https://github.com/espressif/binutils-gdb/releases/download/esp-gdb-v$(version)/riscv32-esp-elf-gdb-$(version)-aarch64-apple-darwin24.5.tar.gz"
            )
            add_versions("16.3_20250913", "92771492084746fd22521c7c5b52bf1ed6dd86ef3cafe60e771bbdb4f0943f5a")
        end
    elseif (os.host() == "windows") then
        if (os.arch() == "x86_64") then
            set_urls(
                "https://github.com/espressif/binutils-gdb/releases/download/esp-gdb-v$(version)/riscv32-esp-elf-gdb-$(version)-x86_64-w64-mingw32.zip"
            )
            add_versions("16.3_20250913", "32e79cb43b40f3b256193139b1fefd2782e3eaf82ee317b757ec8ba18b35159d")
        elseif (os.arch() == "i386") then
            set_urls(
                "https://github.com/espressif/binutils-gdb/releases/download/esp-gdb-v$(version)/riscv32-esp-elf-gdb-$(version)-i686-w64-mingw32.zip"
            )
            add_versions("16.3_20250913", "c6a36c469d3b76e2b442be207814f7c3f71f21faf6faab4dd33fdedd56d89c01")
        end
    end

    on_install("@windows", "@linux", "@macosx", function(package)
        os.vcp("*", package:installdir())
    end)

    on_test(function(package)
        local gdb = "riscv32-esp-elf-gdb"
        if gdb and is_host("windows") then
            gdb = gdb .. ".exe"
        end
        os.vrunv(gdb, { "--version" })
    end)
end)
