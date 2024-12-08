from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get
import conan
import os

class protobufRecipe(ConanFile):
    name = "protobuf"
    description = "Google's data interchange format"
    license = "Google Custom License"
    generators = "CMakeDeps", "CMakeToolchain"
    no_copy_source = True
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "v29.1"
    url = "https://github.com/protocolbuffers/protobuf/archive/refs/tags/{0}.tar.gz".format(version)

    def requirements(self):
        self.requires("zlib/v1.3.1")
        self.requires("abseil-cpp/20240722.0")

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

        variables["CMAKE_PREFIX_PATH"] = os.path.join(self.dependencies["zlib"].package_folder)
        variables["absl_DIR"] = os.path.join(self.dependencies["abseil-cpp"].package_folder, 'lib', 'cmake', 'absl')
        variables["protobuf_ABSL_PROVIDER"] = "package"
        variables["protobuf_BUILD_TESTS"] = convert_to_cmake_boolean(False)

        cmake.configure(variables=variables)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        cmake.install()
        fix_apple_shared_install_name(self)
