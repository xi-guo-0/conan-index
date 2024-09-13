from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps

class sol2Recipe(ConanFile):
    name = "sol2"
    description = "a C++ <-> Lua API wrapper with advanced features and top notch performance"
    license = "MIT"
    generators = "CMakeDeps", "CMakeToolchain"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "v3.3.0"
    url = "https://github.com/ThePhD/sol2.git"

    def source(self):
        git = Git(self)
        git.clone(self.url, target=".", args=["--depth", "1", "--branch", self.version])
        pass

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.install()
