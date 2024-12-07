from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.files import get
import os

class libpngRecipe(ConanFile):
    name = "libpng"
    description = "Portable Network Graphics support"
    license = "PNG Reference Library License version 2"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "v1.6.44"
    url = "https://github.com/pnggroup/libpng/archive/refs/tags/{0}.tar.gz".format(version)

    def requirements(self):
        self.requires("zlib/v1.3.1")

    def source(self):
        get(self, self.url, strip_root=True)

    def generate(self):
        tc = AutotoolsToolchain(self)
        env = tc.environment()
        tc.update_configure_args({
            "--includedir": None,
            "--oldincludedir": None,
            "--sbindir": None,
            "--with-zlib-prefix": self.dependencies["zlib"].package_folder,
        })
        tc.generate(env)

    def build(self):
        autotools = Autotools(self)
        autotools.configure()
        autotools.install()
        fix_apple_shared_install_name(self)
