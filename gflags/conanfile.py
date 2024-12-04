from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get

class gflagsRecipe(ConanFile):
    name = "gflags"
    description = "The gflags package contains a C++ library that implements commandline flags processing"
    license = "BSD-3-Clause"
    generators = "CMakeDeps", "CMakeToolchain"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "v2.2.2"
    url = "https://github.com/gflags/gflags/archive/refs/tags/{0}.tar.gz".format(version)


    def source(self):
        get(self, self.url, strip_root=True)

    def build(self):
        cmake = CMake(self)
        def convert_to_cmake_boolean(value):
            return "ON" if value else "OFF"
        variables = {}
        variables["BUILD_SHARED_LIBS"] = convert_to_cmake_boolean(self.options.shared)
        variables["BUILD_STATIC_LIBS"] = convert_to_cmake_boolean(not self.options.shared)
        variables["CMAKE_CXX_STANDARD"] = self.settings.compiler.cppstd
        variables["CMAKE_POSITION_INDEPENDENT_CODE"] = convert_to_cmake_boolean(True)
        cmake.configure(variables=variables)
        cmake.build()
        cmake.install()
