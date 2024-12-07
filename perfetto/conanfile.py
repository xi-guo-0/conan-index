from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get
import os

class perfettoRecipe(ConanFile):
    name = "perfetto"
    description = "allows userspace applications to emit trace events and add more app-specific context to a Perfetto trace"
    license = "Apache-2.0"
    generators = "CMakeDeps", "CMakeToolchain"
    no_copy_source = True
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "v48.1"
    url = "https://github.com/google/perfetto/archive/refs/tags/{0}.tar.gz".format(version)

    def source(self):
        get(self, self.url, strip_root=True)

    def _generate_cmakelists(self):
        cmake_content = """
cmake_minimum_required(VERSION 3.10)
project(perfetto)
add_library(${PROJECT_NAME} sdk/perfetto.cc)
target_include_directories(${PROJECT_NAME} PUBLIC sdk/perfetto.cc)
install(TARGETS ${PROJECT_NAME}
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        RUNTIME DESTINATION bin)
install(DIRECTORY ${CMAKE_SOURCE_DIR}/sdk/
        DESTINATION include
        FILES_MATCHING PATTERN "*.h" PATTERN "*.hpp")
"""
        cmake_file_path = os.path.join(self.source_folder, "CMakeLists.txt")
        with open(cmake_file_path, "w") as cmake_file:
            cmake_file.write(cmake_content)

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
        self._generate_cmakelists()
        cmake = self.configure_cmake()
        cmake.build()
        cmake.install()
        fix_apple_shared_install_name(self)
