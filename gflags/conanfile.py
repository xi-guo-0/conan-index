from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps

class gflagsRecipe(ConanFile):
    name = "gflags"
    description = "The gflags package contains a C++ library that implements commandline flags processing"
    license = "BSD-3-Clause"
    generators = "CMakeDeps", "CMakeToolchain"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "v2.2.2"
    url = "https://github.com/gflags/gflags.git"

    def source(self):
        git = Git(self)
        git.clone(self.url, target=".", args=["--depth", "1", "--branch", self.version])
        pass

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
