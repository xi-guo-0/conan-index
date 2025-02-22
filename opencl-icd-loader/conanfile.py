from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get


class opencl_icd_loaderRecipe(ConanFile):
    name = "opencl-icd-loader"
    description = "The OpenCL ICD Loader project"
    license = "Apache-2.0"
    generators = "CMakeDeps", "CMakeToolchain"
    no_copy_source = True
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}
    version = "v2024.10.24"
    url = f"https://github.com/KhronosGroup/OpenCL-ICD-Loader/archive/refs/tags/{version}.tar.gz"

    def requirements(self):
        self.requires(f"opencl-headers/{self.version}")

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
        opencl_headers = self.dependencies["opencl-headers"].package_folder
        variables["CMAKE_PREFIX_PATH"] = opencl_headers
        cmake.configure(variables=variables)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        cmake.install()
        fix_apple_shared_install_name(self)
