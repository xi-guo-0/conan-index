from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.scm import Git
import os
import shutil

class ncursesRecipe(ConanFile):
    name = "ncurses"
    description = "ncurses (new curses) is a programming library providing an application programming interface (API) that allows writing text-based user interfaces (TUI) in a computer terminal-independent manner"
    license = "GPL"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "v6.4"
    url = "https://github.com/mirror/ncurses.git"

    def source(self):
        git = Git(self)
        git.clone(self.url, target=".", args=["--depth", "1", "--branch", self.version])

    def generate(self):
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
            env.define("PATH", "{0}/bin:{1}".format(os.getenv("TOOLCHAIN"), os.getenv("PATH")))
            tc.configure_args.append("CC=clang")
            tc.configure_args.append("--without-cxx")
            tc.configure_args.append("--without-cxx-binding")
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
