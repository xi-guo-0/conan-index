from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.files import get
from conan.tools.gnu import Autotools, AutotoolsToolchain
import os

class luaRecipe(ConanFile):
    name = "lua"
    description = "Lua is a powerful, efficient, lightweight, embeddable scripting language"
    license = "MIT"
    generators = "AutotoolsToolchain"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "5.4.6"
    url = "https://www.lua.org/ftp/lua-{0}.tar.gz".format(version)

    def source(self):
        get(self, self.url, strip_root=True)

    def build(self):
        autotools = Autotools(self)
        make_args = []
        if self.settings.os == "Android":
            make_args = ["CC={}".format(os.getenv("CC")),
                         "RANLIB={}".format(os.getenv("RANLIB")),
                         "linux"]
        elif self.settings.os == "QNX":
            make_args = ["CC={}".format(os.getenv("CC")),
                         "RANLIB={}".format(os.getenv("RANLIB")),
                         "posix"]
        autotools.make(args=make_args)
        autotools.install(args=["INSTALL_TOP={0}".format(self.package_folder)])
        fix_apple_shared_install_name(self)
