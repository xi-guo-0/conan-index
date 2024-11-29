from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.files import get
import os

class rubyRecipe(ConanFile):
    name = "ruby"
    description = "an interpreted object-oriented programming language"
    license = "MIT"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "v3_3_6"
    url = "https://github.com/ruby/ruby/archive/refs/tags/{0}.tar.gz".format(version)

    def source(self):
        get(self, self.url, strip_root=True)

    def requirements(self):
        self.requires("openssl/openssl-3.3.1")
        self.requires("libyaml/0.2.5")
        self.requires("zlib/v1.3.1")

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
        tc.configure_args.append("--disable-install-doc")

        openssl_root = self.dependencies["openssl"].package_folder
        libyaml_root = self.dependencies["libyaml"].package_folder
        zlib_root = self.dependencies["zlib"].package_folder
        env.define("CFLAGS", "-I{0}/include -I{1}/include -I{2}/include".format(openssl_root, libyaml_root, zlib_root))
        env.define("LDFLAGS", "-L{0}/lib -L{1}/lib -L{2}/lib".format(openssl_root, libyaml_root, zlib_root))
        tc.generate(env)

    def build(self):
        autotools = Autotools(self)
        self.run("autoreconf -fiv")
        autotools.configure()
        autotools.install()
        fix_apple_shared_install_name(self)
