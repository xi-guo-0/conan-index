from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.files import get
from conan.tools.gnu import Autotools, AutotoolsToolchain
import os


class luaRecipe(ConanFile):
    name = "lua"
    description = (
        "Lua is a powerful, efficient, lightweight, embeddable scripting language"
    )
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

        for env_var in ["CC", "RANLIB"]:
            if os.getenv(env_var):
                make_args.append(f"{env_var}={os.getenv(env_var)}")
                pass  # if
            pass  # for

        if self.settings.os == "Android":
            make_args.append("linux")
            pass  # if
        elif self.settings.os == "Neutrino":
            make_args.append("posix")
            pass  # elif

        autotools.make(args=make_args)
        autotools.install(args=["INSTALL_TOP={0}".format(self.package_folder)])
        fix_apple_shared_install_name(self)
