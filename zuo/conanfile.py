from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.gnu import Autotools, AutotoolsToolchain

class zuoRecipe(ConanFile):
    name = "zuo"
    description = "A tiny Racket for scripting"
    license = "MIT"
    generators = "AutotoolsToolchain"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "v1.10"
    url = "https://github.com/racket/zuo.git"

    def source(self):
        git = Git(self)
        git.clone(self.url, target=".", args=["--depth", "1", "--branch", self.version])
    def build(self):
        autotools = Autotools(self)
        args = []
        autotools.configure(args=args)
        autotools.make()
        autotools.install()
