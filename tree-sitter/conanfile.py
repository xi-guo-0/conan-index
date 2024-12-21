from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get
import os
import shutil

class tree_sitterRecipe(ConanFile):
    name = "tree-sitter"
    description = "An incremental parsing system for programming tools"
    license = "MIT"
    generators = "CMakeDeps", "CMakeToolchain"
    no_copy_source = True
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "v0.24.5"
    url = "https://github.com/tree-sitter/tree-sitter/archive/refs/tags/{0}.tar.gz".format(version)

    def source(self):
        get(self, self.url, strip_root=True)
        destination_dir = self.source_folder
        source_dir = os.path.join(destination_dir, "lib")
        if os.path.exists(source_dir) and os.path.isdir(source_dir):
            for item in os.listdir(source_dir):
                source_path = os.path.join(source_dir, item)
                destination_path = os.path.join(destination_dir, item)
                shutil.move(source_path, destination_path)
                pass # for
            # pass if

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
