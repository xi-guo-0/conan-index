from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get
import conan
import glob
import os

class zlibRecipe(ConanFile):
    name = "zlib"
    description = "a general purpose data compression library"
    license = "MIT"
    generators = "CMakeDeps", "CMakeToolchain"
    no_copy_source = True
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "v1.3.1"
    url = "https://github.com/madler/zlib/archive/refs/tags/{0}.tar.gz".format(version)

    def source(self):
        get(self, self.url, strip_root=True)

    def configure_cmake(self):
        cmake = CMake(self)
        def convert_to_cmake_boolean(value):
            return "ON" if value else "OFF"

        variables = {}
        variables["BUILD_SHARED_LIBS"] = convert_to_cmake_boolean(self.options.shared)
        variables["BUILD_STATIC_LIBS"] = convert_to_cmake_boolean(not self.options.shared)
        variables["CMAKE_CXX_STANDARD"] = self.settings.compiler.cppstd
        variables["CMAKE_POSITION_INDEPENDENT_CODE"] = convert_to_cmake_boolean(True)

        cmake.configure(variables=variables)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        cmake.install()
        fix_apple_shared_install_name(self)
    def package(self):
        if self.options.shared:
            os.remove(os.path.join(self.package_folder, "lib", "libz.a"))
        else:
            lib_dir = os.path.join(self.package_folder, "lib")
            dynamic_libs = glob.glob(os.path.join(lib_dir, "*.so")) + glob.glob(os.path.join(lib_dir, "*.dll")) + glob.glob(os.path.join(lib_dir, "*.dylib"))
            for lib in dynamic_libs:
                if os.path.islink(lib) or os.path.isfile(lib):
                    os.remove(lib)
