from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.files import get

class gperftoolsRecipe(ConanFile):
    name = "gperftools"
    description = "a collection of a high-performance multi-threaded malloc() implementation, plus some pretty nifty performance analysis tools"
    license = "BSD-3-Clause"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "gperftools-2.16"
    url = "https://github.com/gperftools/gperftools/archive/refs/tags/{0}.tar.gz".format(version)

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
        tc.generate(env)

    def build(self):
        autotools = Autotools(self)
        self.run("autoreconf -fiv")
        autotools.configure()
        autotools.install()
        fix_apple_shared_install_name(self)
