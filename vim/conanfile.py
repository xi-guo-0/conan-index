from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.files import get
import conan
import os
import os
import shutil

class vimRecipe(ConanFile):
    name = "vim"
    description = "a highly configurable text editor built to make creating and changing any kind of text very efficient"
    license = "VIM"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "v9.1.0902"
    url = "https://github.com/vim/vim/archive/refs/tags/{0}.tar.gz".format(version)

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
        if self.settings.os == "Android":
            pass
        elif self.settings.os == "QNX":
            conan.tools.files.replace_in_file(self, "src/xxd/Makefile", " -DUNIX ", " ")
            conan.tools.files.replace_in_file(self, "src/auto/configure", " -lrt", " ")
            env.define("vim_cv_uname_output", "QNX")
            env.define("vim_cv_toupper_broken", "set")
            env.define("vim_cv_terminfo", "yes")
            env.define("vim_cv_tgetent", "zero")
            env.define("vim_cv_getcwd_broken", "no")
            env.define("vim_cv_stat_ignores_slash", "no")
            env.define("vim_cv_memmove_handles_overlap", "yes")
            env.define("vim_cv_bcopy_handles_overlap", "yes")
            env.define("vim_cv_memcpy_handles_overlap", "yes")
            env.define("CFLAGS", "-D__LITTLEENDIAN__=1 -D__QNXNTO__=1 -D__QNX__=1 -D_XOPEN_SOURCE=700 -DHAVE_MATH_H=1 -DHAVE_ISNAN=1 -DHAVE_ISINF=1")
            tc.update_configure_args({
                "--target": "aarch64-unknown-nto-qnx7.0.0",
                "--with-tlib": "ncurses",
                "--host": "aarch64-unknown-nto-qnx7.0.0",
            })
            tc.configure_args.append("--disable-gui")
        tc.generate(env)

    def build(self):
        autotools = Autotools(self)
        autotools.configure()
        autotools.install()
        fix_apple_shared_install_name(self)
