package("arm-none-eabi-gcc", function()
    set_kind("toolchain")
    set_homepage("https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads")
    set_description("Arm GNU Toolchain")

    if (os.host() == "linux") then
        if (os.arch() == "x86_64") then
            set_urls(
                "https://developer.arm.com/-/media/Files/downloads/gnu/$(version)/binrel/arm-gnu-toolchain-$(version)-x86_64-arm-none-eabi.tar.xz"
            )
            add_versions("15.2.rel1", "597893282ac8c6ab1a4073977f2362990184599643b4c5ee34870a8215783a16")
            add_versions("14.3.rel1", "8f6903f8ceb084d9227b9ef991490413014d991874a1e34074443c2a72b14dbd")
        elseif (os.arch() == "arm64") then
            set_urls(
                "https://developer.arm.com/-/media/Files/downloads/gnu/$(version)/binrel/arm-gnu-toolchain-$(version)-aarch64-arm-none-eabi.tar.xz"
            )
            add_versions("15.2.rel1", "d061559d814b205ed30c5b7c577c03317ec447ca51cd5a159d26b12a5bbeb20c")
            add_versions("14.3.rel1", "2d465847eb1d05f876270494f51034de9ace9abe87a4222d079f3360240184d3")
        end
    elseif (os.host() == "macosx") then
        if (os.arch() == "x86_64") then
            set_urls(
                "https://developer.arm.com/-/media/Files/downloads/gnu/$(version)/binrel/arm-gnu-toolchain-$(version)-darwin-x86_64-arm-none-eabi.tar.xz"
            )
            add_versions("14.2.rel1", "2d9e717dd4f7751d18936ae1365d25916534105ebcb7583039eff1092b824505")
        elseif (os.arch() == "arm64") then
            set_urls(
                "https://developer.arm.com/-/media/Files/downloads/gnu/$(version)/binrel/arm-gnu-toolchain-$(version)-darwin-arm64-arm-none-eabi.tar.xz"
            )
            add_versions("15.2.rel1", "1938a84b7105c192e3fb4fa5e893ba25f425f7ddab40515ae608cd40f68669a8")
            add_versions("14.3.rel1", "30f4d08b219190a37cded6aa796f4549504902c53cfc3c7e044a8490b6eba1f7")
        end
    elseif (os.host() == "windows") then
        if (os.arch() == "x86_64") then
            set_urls(
                "https://developer.arm.com/-/media/Files/downloads/gnu/$(version)/binrel/arm-gnu-toolchain-$(version)-mingw-w64-x86_64-arm-none-eabi.zip"
            )
            add_versions("15.2.rel1", "b40db54536d2fdf0ff21f4316b56c1fc4d3b782b792c5b298bcbeaf5eccedb96")
            add_versions("14.3.rel1", "836ebe51fd71b6542dd7884c8fb2011192464b16c28e4b38fddc9350daba5ee8")
        elseif (os.arch() == "i386") then
            set_urls(
                "https://developer.arm.com/-/media/Files/downloads/gnu/$(version)/binrel/arm-gnu-toolchain-$(version)-mingw-w64-i686-arm-none-eabi.zip"
            )
            add_versions("15.2.rel1", "7936cac895611023ffb22a64b8e426098c7104cb689778c1894572ca840b9ece")
            add_versions("14.3.rel1", "864c0c8815857d68a1bbba2e5e2782255bb922845c71c97636004a3d74f60986")
        end
    end

    on_install("@windows", "@linux", "@macosx", function(package)
        os.vcp("*", package:installdir())
    end)

    on_test(function(package)
        local gcc = "arm-none-eabi-gcc"
        if gcc and is_host("windows") then
            gcc = gcc .. ".exe"
        end
        os.vrunv(gcc, { "--version" })
    end)
end)
