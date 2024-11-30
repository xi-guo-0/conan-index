from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.files import get
import os

class guileRecipe(ConanFile):
    name = "guile"
    description = "a programming language"
    license = "GNU LGPLv3"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "3.0.10"
    url = "https://ftp.gnu.org/gnu/guile/guile-{0}.tar.gz".format(version)

    def source(self):
        get(self, self.url, strip_root=True)

    def requirements(self):
        self.requires("bdw-gc/v8.2.8")
        self.requires("gmp/6.3.0")
        self.requires("libunistring/1.3")

    def generate(self):
        tc = AutotoolsToolchain(self)
        env = tc.environment()
        tc.update_configure_args({
            "--includedir": None,
            "--oldincludedir": None,
            "--sbindir": None,
            "--with-bdw-gc": "{0}/lib/pkgconfig/bdw-gc.pc".format(self.dependencies["bdw-gc"].package_folder),
            "--with-libgmp-prefix": self.dependencies["gmp"].package_folder,
            "--with-libiconv-prefix": self.dependencies["libiconv"].package_folder,
            "--with-libunistring-prefix": self.dependencies["libunistring"].package_folder,
        })
        tc.generate(env)

    def build(self):
        autotools = Autotools(self)
        autotools.configure()
        autotools.install()
        fix_apple_shared_install_name(self)
