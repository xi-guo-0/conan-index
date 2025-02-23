from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get


class libresslRecipe(ConanFile):
    name = "libressl"
    description = "LibreSSL Portable itself. This includes the build scaffold and compatibility layer that builds portable LibreSSL from the OpenBSD source code"
    license = "Apache-1.0, BSD-4-Clause, ISC, public domain"
    generators = "CMakeDeps", "CMakeToolchain"
    no_copy_source = True
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}
    version = "v4.0.0"
    url = "https://github.com/libressl/portable/releases/download/v{0}/libressl-{0}.tar.gz".format(
        version[1:]
    )

    def source(self):
        get(self, self.url, strip_root=True)

    def configure_cmake(self):
        cmake = CMake(self)

        def convert_to_cmake_boolean(value):
            return "ON" if value else "OFF"

        variables = {}
        variables["BUILD_SHARED_LIBS"] = convert_to_cmake_boolean(self.options.shared)
        variables["BUILD_STATIC_LIBS"] = convert_to_cmake_boolean(
            not self.options.shared
        )
        variables["CMAKE_CXX_STANDARD"] = self.settings.compiler.cppstd
        variables["CMAKE_POSITION_INDEPENDENT_CODE"] = convert_to_cmake_boolean(
            self.options.fPIC
        )
        cmake.configure(variables=variables)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        cmake.install()
        fix_apple_shared_install_name(self)
