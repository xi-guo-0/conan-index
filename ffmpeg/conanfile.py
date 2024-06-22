from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.scm import Git
import os

class ffmpegRecipe(ConanFile):
    name = "ffmpeg"
    description = "FFmpeg is a collection of libraries and tools to process multimedia content such as audio, video, subtitles and related metadata"
    license = "LGPL"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "n7.0.1"
    url = "https://github.com/FFmpeg/FFmpeg.git"

    def source(self):
        git = Git(self)
        git.clone(self.url, target=".", args=["--depth", "1", "--branch", self.version])

    def generate(self):
        tc = AutotoolsToolchain(self)
        env = tc.environment()
        tc.update_configure_args({
            "--includedir": None,
            "--oldincludedir": None,
            "--sbindir": None,
        })
        if self.settings.os == "Android":
            env.unset("CPPFLAGS")
            env.unset("LDFLAGS")
            ndk_bin = "{0}/toolchains/llvm/prebuilt/darwin-x86_64/bin".format(os.getenv("ANDROID_NDK"))
            tc.update_configure_args({
                "--arch": "aarch64",
                "--build": None,
                "--cc": "{}/aarch64-linux-android34-clang".format(ndk_bin),
                "--host": None,
                "--strip": "{}/llvm-strip".format(ndk_bin),
                "--target-os": "android",
            })
        tc.configure_args.append("--enable-cross-compile")
        tc.generate(env)

    def build(self):
        autotools = Autotools(self)
        autotools.configure(args=["--disable-doc"])
        autotools.make()
        autotools.install()
        fix_apple_shared_install_name(self)
