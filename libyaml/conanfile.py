from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.files import get
import os

class libyamlRecipe(ConanFile):
    name = "libyaml"
    description = "A C library for parsing and emitting YAML"
    license = "MIT"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "0.2.5"
    url = "https://github.com/yaml/libyaml/archive/refs/tags/0.2.5.tar.gz".format(version)

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
        tc.generate(env)

    def build(self):
        autotools = Autotools(self)
        self.run("./bootstrap")
        autotools.configure()
        autotools.install()
        fix_apple_shared_install_name(self)
