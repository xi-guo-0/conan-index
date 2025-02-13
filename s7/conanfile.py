from conan import ConanFile
from conan.tools.cmake import CMake
from conan.tools.files import get
import os


class s7Recipe(ConanFile):
    name = "s7"
    description = "a Scheme interpreter"
    license = "0-clause BSD"
    generators = "CMakeDeps", "CMakeToolchain"
    no_copy_source = True
    settings = "os", "arch", "compiler", "build_type"
    version = "latest"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    url = "https://ccrma.stanford.edu/software/s7/s7.tar.gz"

    def source(self):
        get(self, self.url, strip_root=True)

    def _generate_cmakelists(self):
        cmake_content = """
cmake_minimum_required(VERSION 3.10)
project(s7)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
list(APPEND CMAKE_CXX_STANDARD_INCLUDE_DIRECTORIES
     ${CMAKE_CXX_IMPLICIT_INCLUDE_DIRECTORIES})

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

add_executable(${PROJECT_NAME} s7.c)
target_compile_definitions(${PROJECT_NAME} PUBLIC WITH_MAIN=1)
set(DEPS m)
find_library(DL_LIBRARY dl)
if(DL_LIBRARY)
  list(APPEND DEPS ${DL_LIBRARY})
endif()
target_link_libraries(${PROJECT_NAME} ${DEPS})
target_include_directories(${PROJECT_NAME} PUBLIC .)
install(
  TARGETS ${PROJECT_NAME}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin)
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
        variables["BUILD_STATIC_LIBS"] = convert_to_cmake_boolean(
            not self.options.shared
        )
        variables["CMAKE_POSITION_INDEPENDENT_CODE"] = convert_to_cmake_boolean(
            self.options.fPIC
        )
        variables["CMAKE_BUILD_TYPE"] = "Release"
        variables["CMAKE_TRY_COMPILE_CONFIGURATION"] = "Release"

        cmake.configure(variables=variables)
        return cmake

    def build(self):
        self._generate_cmakelists()
        cmake = self.configure_cmake()
        cmake.build()
        cmake.install()
