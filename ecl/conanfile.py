from conan import ConanFile
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.scm import Git


class eclRecipe(ConanFile):
    name = "ecl"
    description = "Embeddable Common-Lisp"
    license = "GNU LGPLv2.1"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "24.5.10"
    url = "https://gitlab.com/embeddable-common-lisp/ecl.git"

    def source(self):
        git = Git(self)
        git.clone(self.url, target=".", args=["--depth", "1", "--branch", self.version])

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
        autotools.configure()
        autotools.make()
        autotools.install()
