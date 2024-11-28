from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.files import get
import os

class cpythonRecipe(ConanFile):
    name = "cpython"
    description = "The Python programming language"
    license = "the PSF License Version 2 and the Zero-Clause BSD license"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "v3.13.0"
    url = "https://github.com/python/cpython/archive/refs/tags/{0}.tar.gz".format(version)

    def source(self):
        get(self, self.url, strip_root=True)

    def requirements(self):
        if self.settings.os == "Android":
            self.requires("bzip2/bzip2-1.0.8")
            self.requires("libffi/v3.4.6")

    def generate(self):
        tc = AutotoolsToolchain(self)
        env = tc.environment()
        tc.update_configure_args({
            "--includedir": None,
            "--oldincludedir": None,
            "--sbindir": None,
        })
        if self.options.shared:
            tc.configure_args.append("--enable-shared")
            tc.update_configure_args({"--enable-static": None})
        else:
            tc.configure_args.append("--enable-static")
            tc.update_configure_args({"--enable-shared": None})
        if self.settings.os == "Android":
            tc.update_configure_args({
                "--host": "aarch64-linux-android"
            })
            tc.configure_args.append("--with-build-python")
            bzip2_root = self.dependencies["bzip2"].package_folder
            libffi_root = self.dependencies["libffi"].package_folder
            env.define("BZIP2_CFLAGS", "-I{0}/include".format(bzip2_root))
            env.define("BZIP2_LIBS", "-L{0}/lib".format(bzip2_root))
            env.define("LIBFFI_CFLAGS", "-I{0}/include".format(libffi_root))
            env.define("LIBFFI_LIBS", "-L{0}/lib".format(libffi_root))
        tc.generate(env)

    def build(self):
        autotools = Autotools(self)
        autotools.configure()
        autotools.make()
        autotools.install()
        fix_apple_shared_install_name(self)
