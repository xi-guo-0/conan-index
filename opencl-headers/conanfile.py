from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get


class opencl_headersRecipe(ConanFile):
    name = "opencl-headers"
    description = "Khronos OpenCL-Headers"
    license = "Apache-2.0"
    generators = "CMakeDeps", "CMakeToolchain"
    no_copy_source = True
    settings = "os", "arch", "compiler", "build_type"
    version = "v2024.10.24"
    url = f"https://github.com/KhronosGroup/OpenCL-Headers/archive/refs/tags/{version}.tar.gz"

    def source(self):
        get(self, self.url, strip_root=True)

    def configure_cmake(self):
        cmake = CMake(self)

        def convert_to_cmake_boolean(value):
            return "ON" if value else "OFF"

        variables = {}
        variables["BUILD_TESTING"] = convert_to_cmake_boolean(False)
        variables["OPENCL_HEADERS_BUILD_TESTING"] = convert_to_cmake_boolean(False)
        variables["OPENCL_HEADERS_BUILD_CXX_TESTS"] = convert_to_cmake_boolean(False)
        cmake.configure(variables=variables)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        cmake.install()
