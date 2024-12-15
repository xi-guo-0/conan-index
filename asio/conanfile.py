from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.files import get
import os
import shutil

class asioRecipe(ConanFile):
    name = "asio"
    description = "Asio C++ Library"
    license = "Boost Software License"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "asio-1-32-0"
    url = "https://github.com/chriskohlhoff/asio/archive/refs/tags/{0}.tar.gz".format(version)

    def requirements(self):
        self.requires("openssl/openssl-3.4.0")

    def source(self):
        get(self, self.url, strip_root=True)

    def generate(self):
        tc = AutotoolsToolchain(self)
        env = tc.environment()
        tc.update_configure_args({
            "--includedir": None,
            "--oldincludedir": None,
            "--sbindir": None,
            "--with-openssl": self.dependencies["openssl"].package_folder,
        })
        tc.generate(env)

    def build(self):
        source_dir = 'asio'
        if os.path.exists(source_dir) and os.path.isdir(source_dir):
            for item in os.listdir(source_dir):
                source_path = os.path.join(source_dir, item)
                destination_path = item
                shutil.move(source_path, destination_path)
                pass # for
            pass # if
        os.rmdir(source_dir)
        self.run("autoreconf -fiv")
        autotools = Autotools(self)
        autotools.configure()
        autotools.install()
