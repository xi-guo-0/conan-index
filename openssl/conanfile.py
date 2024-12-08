from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.files import get
import os
import platform
import shutil

class opensslRecipe(ConanFile):
    name = "openssl"
    description = "TLS/SSL and crypto library"
    license = "Apache-2.0"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "openssl-3.4.0"
    url = "https://github.com/openssl/openssl/archive/refs/tags/{0}.tar.gz".format(version)

    def source(self):
        get(self, self.url, strip_root=True)

    def generate(self):
        shutil.move("Configure", "configure")
        tc = AutotoolsToolchain(self)
        env = tc.environment()
        tc.update_configure_args({
            "--bindir": None,
            "--disable-shared": None,
            "--enable-static": None,
            "--includedir": None,
            "--libdir": None,
            "--oldincludedir": None,
            "--sbindir": None
        })

        if self.options.shared:
            tc.configure_args.append("no-static")
        else:
            tc.configure_args.append("no-shared")

        if self.settings.os == "Macos":
            tc.configure_args.append("CC=clang")
            tc.configure_args.append("darwin64-arm64")
        elif self.settings.os == "Android":
            os_name = platform.system()
            ANDROID_NDK_BIN = "{0}/toolchains/llvm/prebuilt/linux-x86_64/bin".format(os.getenv("ANDROID_NDK"))
            if os_name == "Darwin":
                ANDROID_NDK_BIN = "{0}/toolchains/llvm/prebuilt/darwin-x86_64/bin".format(os.getenv("ANDROID_NDK"))
            env.define("PATH", "{0}:{1}".format(ANDROID_NDK_BIN, os.getenv("PATH")))
            tc.configure_args.append("android-arm64")
            tc.configure_args.append("CC=clang")
            tc.configure_args.append("-D__ANDROID_API__={}".format(self.settings.os.api_level))
            tc.update_configure_args({
                "--build": None,
                "--disable-shared": None,
                "--host": None
            })
        tc.generate(env)

    def build(self):
        autotools = Autotools(self)
        autotools.configure()
        autotools.make()
        autotools.install()
        fix_apple_shared_install_name(self)
