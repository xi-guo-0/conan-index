from conan import ConanFile
from conan.tools.files import get
from conan.tools.gnu import Autotools, AutotoolsToolchain


class biglooRecipe(ConanFile):
    name = "bigloo"
    description = "a strict-parenthetical-function programming language"
    license = "GPL"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}
    version = "latest"
    url = "https://www-sop.inria.fr/indes/fp/Bigloo/download/bigloo-latest.tar.gz"

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
                "--enable-shared": None,
                "--disable-static": None,
            }
        )
        tc.generate(env)

    def build(self):
        autotools = Autotools(self)
        autotools.configure()
        autotools.make()
        autotools.install()
