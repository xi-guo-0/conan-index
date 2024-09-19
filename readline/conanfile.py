from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.scm import Git
import os
import shutil

class readlineRecipe(ConanFile):
    name = "readline"
    description = "get a line from a user with editing"
    license = "GPL"
    settings = "os", "arch", "compiler"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "readline-8.2"
    url = "https://git.savannah.gnu.org/git/readline.git"

    def source(self):
        git = Git(self)
        git.clone(self.url, target=".", args=["--depth", "1", "--branch", self.version])

    def generate(self):
        tc = AutotoolsToolchain(self)
        env = tc.environment()
        tc.update_configure_args({
            "--bindir": None,
            "--disable-shared": None,
            "--includedir": None,
            "--libdir": None,
            "--oldincludedir": None,
            "--sbindir": None
        })
        if self.options.shared:
            tc.update_configure_args({
                "--enable-static": "NO",
            })
        else:
            tc.update_configure_args({
                "--enable-shared": "NO",
            })

        if self.settings.os == "Macos":
            tc.configure_args.append("CC=clang")
            tc.configure_args.append("darwin64-arm64")
        elif self.settings.os == "Android":
            env.define("PATH", "{0}/toolchains/llvm/prebuilt/linux-x86_64/bin:{1}".format(os.getenv("ANDROID_NDK"), os.getenv("PATH")))
            tc.configure_args.append("CC=aarch64-linux-android30-clang")
            tc.configure_args.append("--disable-stripping")
            tc.configure_args.append("--without-cxx")
            tc.configure_args.append("--without-cxx-binding")
            tc.update_configure_args({
                "--build": None,
                "--disable-shared": None,
                "--host": "aarch64-linux-android"
            })
        tc.generate(env)

    def build(self):
        autotools = Autotools(self)
        autotools.configure()
        autotools.make()
        autotools.install()
        fix_apple_shared_install_name(self)
