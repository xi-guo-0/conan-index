from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.files import get
import os

class graphvizRecipe(ConanFile):
    name = "graphviz"
    description = "Graphviz is open source graph visualization software"
    license = "Common Public License Version 1.0"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "12.2.0"
    url = "https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/{0}/graphviz-{0}.tar.gz".format(version)

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
        autotools.configure()
        autotools.make()
        autotools.install()
        fix_apple_shared_install_name(self)
