from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.scm import Git
import conan

class leveldbRecipe(ConanFile):
    name = "leveldb"
    description = "a fast key-value storage library"
    license = "BSD-3-Clause"
    generators = "CMakeDeps", "CMakeToolchain"
    no_copy_source = True
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "1.23"
    url = "https://github.com/google/leveldb.git"

    def source(self):
        git = Git(self)
        git.clone(self.url, target=".", args=["--depth", "1", "--branch", self.version])
        self.run("git submodule update --init --recursive --depth 1")
        conan.tools.files.replace_in_file(self, "third_party/benchmark/CMakeLists.txt", '''add_cxx_compiler_flag(-Werror RELEASE)''', "")

    def configure_cmake(self):
        cmake = CMake(self)
        def convert_to_cmake_boolean(value):
            return "ON" if value else "OFF"

        variables = {}
        variables["BUILD_SHARED_LIBS"] = convert_to_cmake_boolean(self.options.shared)
        variables["BUILD_STATIC_LIBS"] = convert_to_cmake_boolean(not self.options.shared)
        variables["CMAKE_CXX_STANDARD"] = self.settings.compiler.cppstd
        variables["CMAKE_POSITION_INDEPENDENT_CODE"] = convert_to_cmake_boolean(self.options.fPIC)

        variables["LEVELDB_BUILD_BENCHMARKS"] = convert_to_cmake_boolean(False)
        variables["LEVELDB_BUILD_TESTS"] = convert_to_cmake_boolean(False)

        cmake.configure(variables=variables)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        cmake.install()
        fix_apple_shared_install_name(self)
