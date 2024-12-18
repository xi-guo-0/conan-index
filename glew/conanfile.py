from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get
import os

class glewRecipe(ConanFile):
    name = "glew"
    description = "a cross-platform open-source C/C++ extension loading library"
    license = "MIT-style or X11-style"
    generators = "CMakeDeps", "CMakeToolchain"
    no_copy_source = True
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "glew-2.2.0"
    url = "https://github.com/nigels-com/glew/releases/download/{0}/{0}.zip".format(version)

    def source(self):
        get(self, self.url, strip_root=True)
        self._generate_cmakelists()

    def _generate_cmakelists(self):
        cmake_content = """
cmake_minimum_required(VERSION 3.10)
project(glew)
add_library(${PROJECT_NAME} src/glew.c)
target_include_directories(${PROJECT_NAME} PUBLIC include)
find_library(OpenGL OpenGL REQUIRED)
target_link_libraries(${PROJECT_NAME} PUBLIC ${OpenGL})
add_executable(glewinfo src/glewinfo.c)
target_include_directories(glewinfo PUBLIC include)
target_link_libraries(glewinfo PUBLIC ${PROJECT_NAME})
add_executable(visualinfo src/visualinfo.c)
target_include_directories(visualinfo PUBLIC include)
target_link_libraries(visualinfo PUBLIC ${PROJECT_NAME})
install(TARGETS ${PROJECT_NAME}
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        RUNTIME DESTINATION bin)
install(TARGETS glewinfo
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        RUNTIME DESTINATION bin)
install(TARGETS visualinfo
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        RUNTIME DESTINATION bin)
install(DIRECTORY ${CMAKE_SOURCE_DIR}/include/GL/
        DESTINATION include/GL
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
        variables["CMAKE_POSITION_INDEPENDENT_CODE"] = convert_to_cmake_boolean(self.options.fPIC)

        cmake.configure(variables=variables)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        cmake.install()
        fix_apple_shared_install_name(self)
