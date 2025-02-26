from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.files import get
import os
import platform


class ncursesRecipe(ConanFile):
    name = "ncurses"
    description = "ncurses (new curses) is a programming library providing an application programming interface (API) that allows writing text-based user interfaces (TUI) in a computer terminal-independent manner"
    license = "GPL"
    settings = "os", "arch", "compiler"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "v6.4"
    url = "https://github.com/mirror/ncurses/archive/refs/tags/{0}.tar.gz".format(
        version
    )

    def source(self):
        get(self, self.url, strip_root=True)

    def generate(self):
        tc = AutotoolsToolchain(self)
        env = tc.environment()
        tc.update_configure_args(
            {
                "--bindir": None,
                "--disable-shared": None,
                "--enable-static": None,
                "--includedir": None,
                "--libdir": None,
                "--oldincludedir": None,
                "--sbindir": None,
            }
        )
        for env_var in ["CC", "RANLIB", "STRIP"]:
            if os.getenv(env_var):
                tc.configure_args.append(f"{env_var}={os.getenv(env_var)}")
                pass  # if
            pass  # for
        if self.settings.os == "Macos":
            tc.configure_args.append("CC=clang")
            tc.configure_args.append("darwin64-arm64")
        elif self.settings.os == "Android":
            os_name = platform.system()
            ANDROID_NDK_BIN = "{0}/toolchains/llvm/prebuilt/linux-x86_64/bin".format(
                os.getenv("ANDROID_NDK")
            )
            if os_name == "Darwin":
                ANDROID_NDK_BIN = (
                    "{0}/toolchains/llvm/prebuilt/darwin-x86_64/bin".format(
                        os.getenv("ANDROID_NDK")
                    )
                )
            env.define("PATH", "{0}:{1}".format(ANDROID_NDK_BIN, os.getenv("PATH")))
            tc.configure_args.append("CC=aarch64-linux-android30-clang")
            tc.configure_args.append("--disable-stripping")
            tc.configure_args.append("--without-cxx")
            tc.configure_args.append("--without-cxx-binding")
            tc.update_configure_args(
                {
                    "--build": None,
                    "--disable-shared": None,
                    "--host": "aarch64-linux-android",
                }
            )
        elif self.settings.arch == "armv8" and self.settings.os == "Linux":
            tc.configure_args.append("--disable-stripping")
            tc.update_configure_args(
                {
                    "--build": None,
                    "--disable-shared": None,
                    "--host": "aarch64-linux-gnu",
                }
            )
        tc.generate(env)

    def build(self):
        autotools = Autotools(self)
        autotools.configure()
        autotools.make()
        autotools.install()
        fix_apple_shared_install_name(self)
