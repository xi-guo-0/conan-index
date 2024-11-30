from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.files import get
import os

class libunistringRecipe(ConanFile):
    name = "libunistring"
    description = "This library provides functions for manipulating Unicode strings and for manipulating C strings according to the Unicode standard"
    license = "the GNU LGPLv3+ or the GNU GPLv2+"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "1.3"
    url = "https://ftp.gnu.org/gnu/libunistring/libunistring-{0}.tar.gz".format(version)

    def requirements(self):
        self.requires("libiconv/1.17")

    def source(self):
        get(self, self.url, strip_root=True)

    def generate(self):
        tc = AutotoolsToolchain(self)
        env = tc.environment()
        tc.update_configure_args({
            "--includedir": None,
            "--oldincludedir": None,
            "--sbindir": None,
            "--with-libiconv-prefix": self.dependencies["libiconv"].package_folder,
        })
        tc.generate(env)

    def build(self):
        autotools = Autotools(self)
        autotools.configure()
        autotools.install()
        fix_apple_shared_install_name(self)
