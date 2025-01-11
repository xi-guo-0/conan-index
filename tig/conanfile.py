from conan import ConanFile
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.files import get


class rubyRecipe(ConanFile):
    name = "ruby"
    description = "Text-mode interface for git"
    license = "GPL-2.0"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "tig-2.5.10"
    url = "https://github.com/jonas/tig/archive/refs/tags/{0}.tar.gz".format(version)

    def source(self):
        get(self, self.url, strip_root=True)

    def generate(self):
        tc = AutotoolsToolchain(self)
        env = tc.environment()
        tc.update_configure_args(
            {
                "--includedir": None,
                "--oldincludedir": None,
                "--sbindir": None,
            }
        )
        tc.generate(env)

    def build(self):
        autotools = Autotools(self)
        self.run("autoreconf -fiv")
        autotools.configure()
        autotools.install()
