from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.scm import Git
import os
import shutil

class opensslRecipe(ConanFile):
    name = "openssl"
    description = "TLS/SSL and crypto library"
    license = "Apache-2.0"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "openssl-3.3.1"
    url = "https://github.com/openssl/openssl.git"

    def source(self):
        git = Git(self)
        git.clone(self.url, target=".", args=["--depth", "1", "--branch", self.version])

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
        if self.settings.os == "Macos":
            tc.configure_args.append("CC=clang")
            tc.configure_args.append("darwin64-arm64")
        elif self.settings.os == "Android":
            env.define("PATH", "{0}/toolchains/llvm/prebuilt/darwin-x86_64/bin:{1}".format(os.getenv("ANDROID_NDK"), os.getenv("PATH")))
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
