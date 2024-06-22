from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.scm import Git
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.env import Environment
import os

class opensshRecipe(ConanFile):
    name = "openssh"
    description = "Portable OpenSSH"
    license = "BSD"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    requires = "openssl/openssl-3.3.1"
    version = "v_9_7_p1"
    url = "https://github.com/openssh/openssh-portable.git"

    def source(self):
        git = Git(self)
        git.clone(self.url, target=".", args=["--depth", "1", "--branch", self.version.upper()])

    def generate(self):
        env = Environment()
        env.define("C_INCLUDE_PATH", os.path.join(self.dependencies["openssl"].package_folder, "include"))
        env.define("LIBRARY_PATH", os.path.join(self.dependencies["openssl"].package_folder, "lib"))
        env.define("DYLD_LIBRARY_PATH", os.path.join(self.dependencies["openssl"].package_folder, "lib"))
        envvars = env.vars(self, scope="build")
        envvars.save_script("my_env")
        tc = AutotoolsToolchain(self)
        tc.update_configure_args({
            "--bindir": None,
            "--disable-shared": None,
            "--enable-static": None,
            "--includedir": None,
            "--libdir": None,
            "--oldincludedir": None,
            "--sbindir": None,
            "--with-ssl-dir": self.dependencies["openssl"].package_folder
        })
        tc.generate()

    def build(self):
        autotools = Autotools(self)
        autotools.autoreconf()
        autotools.configure()
        autotools.make()
