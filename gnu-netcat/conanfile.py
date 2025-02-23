from conan import ConanFile
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.files import get


class gnu_netcatRecipe(ConanFile):
    name = "gnu-netcat"
    description = "a featured networking utility which reads and writes data across network connections, using the TCP/IP protocol"
    license = "GPL"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}
    version = "0.7.1"
    url = f"http://sourceforge.net/projects/netcat/files/netcat/{version}/netcat-{version}.tar.gz"

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
