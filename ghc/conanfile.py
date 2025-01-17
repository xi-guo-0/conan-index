from conan import ConanFile
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.scm import Git

class ghcRecipe(ConanFile):
    name = "ghc"
    description = "Glasgow Haskell Compiler"
    license = "BSD"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}
    version = "ghc-9.12.1"
    url = "https://github.com/ghc/ghc.git"

    def source(self):
        git = Git(self)
        git.clone(self.url, target=".", args=["--depth", "1", "--branch", self.version])
        self.run("git submodule update --init --recursive --depth 1")

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
        self.run("./boot")
        autotools.configure()
        self.run("./hadrian/build")
        autotools.install()
