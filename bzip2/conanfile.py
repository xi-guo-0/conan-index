from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.scm import Git
import os

class bzip2Recipe(ConanFile):
    name = "bzip2"
    description = "a free and open-source file compression program that uses the Burrows–Wheeler algorithm"
    license = "Modified zlib license"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "bzip2-1.0.8"
    url = "https://sourceware.org/git/bzip2.git"

    def source(self):
        git = Git(self)
        git.clone(self.url, target=".", args=["--depth", "1", "--branch", self.version])

    def generate(self):
        tc = AutotoolsToolchain(self)
        env = tc.environment()
        tc.update_configure_args({
            "--includedir": None,
            "--oldincludedir": None,
            "--sbindir": None,
        })
        tc.generate(env)

    def build(self):
        autotools = Autotools(self)
        autotools.install(args=["PREFIX={0}".format(self.package_folder)])
        fix_apple_shared_install_name(self)
