from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get

class libjpeg_turboRecipe(ConanFile):
    name = "libjpeg-turbo"
    description = "a JPEG image codec that uses SIMD instructions to accelerate baseline JPEG compression and decompression on x86, x86-64, Arm, PowerPC, and MIPS systems, as well as progressive JPEG compression on x86, x86-64, and Arm systems"
    license = " IJG and BSD-3-Clause"
    generators = "CMakeDeps", "CMakeToolchain"
    no_copy_source = True
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "3.1.0"
    url = "https://github.com/libjpeg-turbo/libjpeg-turbo/archive/refs/tags/{0}.tar.gz".format(version)

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

        variables["CMAKE_INSTALL_BINDIR"] = "{0}/bin".format(self.package_folder)
        variables["CMAKE_INSTALL_INCLUDEDIR"] = "{0}/include".format(self.package_folder)
        variables["CMAKE_INSTALL_LIBDIR"] = "{0}/lib".format(self.package_folder)
        variables["CMAKE_INSTALL_LIBEXECDIR"] = "{0}/libexec".format(self.package_folder)
        variables["CMAKE_INSTALL_OLDINCLUDEDIR"] = "{0}/oldinclude".format(self.package_folder)
        variables["CMAKE_INSTALL_SBINDIR"] = "{0}/sbin".format(self.package_folder)
        variables["ENABLE_SHARED"] = convert_to_cmake_boolean(self.options.shared)
        variables["ENABLE_STATIC"] = convert_to_cmake_boolean(not self.options.shared)
        variables["WITH_JPEG8"] = convert_to_cmake_boolean(True)

        cmake.configure(variables=variables)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        cmake.install()
        fix_apple_shared_install_name(self)
