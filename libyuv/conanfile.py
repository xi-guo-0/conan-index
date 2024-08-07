import conan
import os
import re
import random
import shutil
from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps

class libyuvRecipe(ConanFile):
    name = "libyuv"
    description = "An open source project that includes YUV scaling and conversion functionality"
    license = "BSD-3-Clause license"
    generators = "CMakeDeps", "CMakeToolchain"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    url = "https://chromium.googlesource.com/libyuv/libyuv"
    commit_id = "f94b8cf7"

    def set_version(self):
        tmp_folder = "/tmp/libyuv-get-version"
        self.run('git clone {0} {1} && cd {1} && git checkout {2}'.format(self.url, tmp_folder, self.commit_id))

        with open('{}/include/libyuv/version.h'.format(tmp_folder), 'r') as file:
            content = file.read()
            self.version = 'v{}-{}'.format(re.search(r'#define LIBYUV_VERSION (\d+)', content).group(1), self.commit_id)
            print("LIBYUV_VERSION: {}".format(self.version))
        shutil.rmtree(tmp_folder)

    def source(self):
        self.run('git clone {0} . && git checkout {1}'.format(self.url, self.commit_id))

    def configure_cmake(self):
        cmake = CMake(self)
        if self.options.shared:
            conan.tools.files.replace_in_file(self, "CMakeLists.txt", "INSTALL ( TARGETS ${ly_lib_static}					DESTINATION lib )", "")
        else:
            conan.tools.files.replace_in_file(self, "CMakeLists.txt", "INSTALL ( TARGETS ${ly_lib_shared} LIBRARY				DESTINATION lib RUNTIME DESTINATION bin )", "")

        variables = {}
        def convert_to_cmake_boolean(value):
            return "ON" if value else "OFF"
        variables["CMAKE_POSITION_INDEPENDENT_CODE"] = convert_to_cmake_boolean(True)
        variables["CMAKE_BUILD_TYPE"] = "Release"
        variables["CMAKE_TRY_COMPILE_CONFIGURATION"] = "Release"

        cmake.configure(variables=variables)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        cmake.install()
