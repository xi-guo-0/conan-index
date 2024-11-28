from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.files import get
import os

class libffiRecipe(ConanFile):
    name = "libffi"
    description = "A portable foreign-function interface library"
    license = "MIT license"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "v3.4.6"
    url = "https://github.com/libffi/libffi/archive/refs/tags/{0}.tar.gz".format(version)

    def source(self):
        get(self, self.url, strip_root=True)

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
            tc.configure_args.append("--disable-docs")
            tc.configure_args.append("--disable-multi-os-directory")
            tc.update_configure_args({
                "--host": "aarch64-linux-android"
            })
        tc.generate(env)

    def build(self):
        autotools = Autotools(self)
        self.run("autoreconf -fiv")
        autotools.configure()
        autotools.install()
        fix_apple_shared_install_name(self)
