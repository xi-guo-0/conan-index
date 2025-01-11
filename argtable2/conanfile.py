from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.cmake import CMake
from conan.tools.files import get
import conan

class argtable2Recipe(ConanFile):
    name = "argtable2"
    description = "A single-file, ANSI C, command-line parsing library that parses GNU-style command-line options"
    license = ""
    generators = "CMakeDeps", "CMakeToolchain"
    no_copy_source = True
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "argtable2-13"
    url = "http://prdownloads.sourceforge.net/argtable/{0}.tar.gz".format(version)

    def source(self):
        get(self, self.url, strip_root=True)
        conan.tools.files.replace_in_file(self, "CMakeLists.txt", "ADD_SUBDIRECTORY( src )", """ADD_SUBDIRECTORY( src )
install(TARGETS argtable2
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        RUNTIME DESTINATION bin)
install(DIRECTORY ${CMAKE_SOURCE_DIR}/src/
        DESTINATION include
        FILES_MATCHING PATTERN "*.h")
""")
        conan.tools.files.replace_in_file(self, "src/arg_int.c", "#include <limits.h>", """#include <limits.h>
#include <ctype.h>""")

    def configure_cmake(self):
        cmake = CMake(self)
        def convert_to_cmake_boolean(value):
            return "ON" if value else "OFF"

        variables = {}
        variables["BUILD_SHARED_LIBS"] = convert_to_cmake_boolean(self.options.shared)
        variables["BUILD_STATIC_LIBS"] = convert_to_cmake_boolean(not self.options.shared)
        variables["CMAKE_CXX_STANDARD"] = self.settings.compiler.cppstd
        variables["CMAKE_POSITION_INDEPENDENT_CODE"] = convert_to_cmake_boolean(self.options.fPIC)
        variables["HAVE_STRINGS_H"] = convert_to_cmake_boolean(True)

        cmake.configure(variables=variables)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        cmake.install()
        fix_apple_shared_install_name(self)
