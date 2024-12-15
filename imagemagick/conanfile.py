from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.files import get
import os

class imagemagickRecipe(ConanFile):
    name = "imagemagick"
    description = "a free and open-source software suite, used for editing and manipulating digital image"
    license = "ImageMagick"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "7.1.1-41"
    url = "https://github.com/ImageMagick/ImageMagick/archive/refs/tags/{0}.tar.gz".format(version)

    def requirements(self):
        self.requires("libjpeg-turbo/3.1.0")

    def source(self):
        get(self, self.url, strip_root=True)

    def generate(self):
        tc = AutotoolsToolchain(self)
        env = tc.environment()
        libjpeg_turbo = self.dependencies["libjpeg-turbo"].package_folder
        env.define("CFLAGS", "-I{0}/include".format(libjpeg_turbo))
        env.define("LDFLAGS", "-L{0}/lib".format(libjpeg_turbo))
        tc.configure_args.append("--without-jxl")
        tc.configure_args.append("--without-lqr")
        tc.update_configure_args({
            "--includedir": None,
            "--oldincludedir": None,
            "--sbindir": None,
        })
        tc.generate(env)

    def build(self):
        autotools = Autotools(self)
        autotools.configure()
        autotools.install()
        fix_apple_shared_install_name(self)
