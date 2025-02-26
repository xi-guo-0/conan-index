from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.files import get
import conan


class vimRecipe(ConanFile):
    name = "vim"
    description = "a highly configurable text editor built to make creating and changing any kind of text very efficient"
    license = "VIM"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "v9.1.0902"
    url = "https://github.com/vim/vim/archive/refs/tags/{0}.tar.gz".format(version)

    def requirements(self):
        if self.settings.arch == "armv8" and (
            self.settings.os == "Android" or self.settings.os == "Linux"
        ):
            self.requires("ncurses/v6.4")

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
        if self.settings.os == "Android":
            # Set the HOME environment variable to /data/local/tmp because Android does not set a default root user directory,
            # which results in the root user's HOME being set to the root directory (/), and the root directory is not writable.
            # echo 'export HOME="/data/local/tmp"' >> /etc/profile

            # Create the .vimrc configuration file in /data/local/tmp so that Vim can read the default configuration.
            # This directory is writable and avoids issues with read-only directories like / or /root.
            # touch /data/local/tmp/.vimrc

            conan.tools.files.replace_in_file(self, "src/auto/configure", " -lrt", " ")
            env.define("vim_cv_getcwd_broken", "no")
            env.define("vim_cv_memmove_handles_overlap", "yes")
            env.define("vim_cv_stat_ignores_slash", "no")
            env.define("vim_cv_terminfo", "yes")
            env.define("vim_cv_tgetent", "zero")
            env.define("vim_cv_toupper_broken", "no")
            env.define("vim_cv_tty_group", "world")
            env.define("vim_cv_uname_output", "Android")
            tc.update_configure_args(
                {
                    "--enable-gui": "no",
                    "--enable-netbeans": "no",
                    "--host": "aarch64-linux-android",
                    "--target": "aarch64-linux-android",
                    "--with-features": "huge",
                    "--with-tlib": "ncurses",
                }
            )
            tc.configure_args.append("--enable-multibyte")
            tc.configure_args.append("--without-x")
            ncurses = self.dependencies["ncurses"].package_folder
            env.define("CFLAGS", "-I{0}/include".format(ncurses))
            env.define("LDFLAGS", "-L{0}/lib".format(ncurses))
        elif self.settings.os == "Neutrino":
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
            env.define(
                "CFLAGS",
                "-D__LITTLEENDIAN__=1 -D__QNXNTO__=1 -D__QNX__=1 -D_XOPEN_SOURCE=700 -DHAVE_MATH_H=1 -DHAVE_ISNAN=1 -DHAVE_ISINF=1",
            )
            tc.update_configure_args(
                {
                    "--target": "ntoaarch64",
                    "--with-tlib": "ncurses",
                    "--host": "ntoaarch64",
                }
            )
            tc.configure_args.append("--disable-gui")
        elif self.settings.arch == "armv8" and self.settings.os == "Linux":
            env.define("vim_cv_getcwd_broken", "no")
            env.define("vim_cv_memmove_handles_overlap", "yes")
            env.define("vim_cv_stat_ignores_slash", "no")
            env.define("vim_cv_terminfo", "yes")
            env.define("vim_cv_tgetent", "zero")
            env.define("vim_cv_toupper_broken", "no")
            env.define("vim_cv_tty_group", "world")
            env.define("vim_cv_uname_output", "ArmLinux")
            tc.update_configure_args(
                {
                    "--enable-gui": "no",
                    "--enable-netbeans": "no",
                    "--host": "aarch64-linux-gnu",
                    "--target": "aarch64-linux-gnu",
                    "--with-features": "huge",
                    "--with-tlib": "ncurses",
                }
            )
            tc.configure_args.append("--enable-multibyte")
            tc.configure_args.append("--without-x")
            ncurses = self.dependencies["ncurses"].package_folder
            env.define("CFLAGS", "-I{0}/include".format(ncurses))
            env.define("LDFLAGS", "-L{0}/lib".format(ncurses))
            tc.configure_args.append("--disable-gui")
            pass
        tc.generate(env)

    def build(self):
        autotools = Autotools(self)
        autotools.configure()
        autotools.install()
        fix_apple_shared_install_name(self)
