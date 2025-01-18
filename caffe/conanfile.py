from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get
import conan


class caffeRecipe(ConanFile):
    name = "caffe"
    description = "a fast open framework for deep learning"
    license = "BSD 2-Clause"
    generators = "CMakeDeps", "CMakeToolchain"
    no_copy_source = True
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}
    version = "1.0"
    url = "https://github.com/BVLC/caffe/archive/refs/tags/{0}.tar.gz".format(version)

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
        variables["CMAKE_POSITION_INDEPENDENT_CODE"] = convert_to_cmake_boolean(True)

        if self.settings.os == "Macos":
            variables["CMAKE_PREFIX_PATH"] = (
                "/opt/homebrew/opt/gflags;/opt/homebrew/opt/glog;/opt/homebrew/opt/protobuf;/opt/homebrew/opt/hdf5;/opt/homebrew/opt/libaec"
            )
            variables["BUILD_python"] = convert_to_cmake_boolean(False)
            variables["USE_LEVELDB"] = convert_to_cmake_boolean(False)
            conan.tools.files.replace_in_file(
                self,
                "{0}/cmake/External/gflags.cmake".format(self.source_folder),
                "find_package(GFlags)",
                "find_package(GFLAGS)",
            )
            conan.tools.files.replace_in_file(
                self,
                "{0}/cmake/External/glog.cmake".format(self.source_folder),
                """find_package(Glog)""",
                """find_package(glog)
set(GLOG_FOUND True)
""",
            )
            conan.tools.files.replace_in_file(
                self,
                "{0}/cmake/ProtoBuf.cmake".format(self.source_folder),
                """${GOOGLE_PROTOBUF_VERSION}""",
                """${Protobuf_VERSION}""",
            )
            conan.tools.files.replace_in_file(
                self,
                "{0}/cmake/ProtoBuf.cmake".format(self.source_folder),
                """find_package( Protobuf REQUIRED )""",
                """
find_package(absl REQUIRED)
include_directories(/opt/homebrew/opt/abseil/include)
find_package(Protobuf REQUIRED)
include(/opt/homebrew/opt/protobuf/lib/cmake/protobuf/protobuf-module.cmake)
set(PROTOBUF_INCLUDE_DIR /opt/homebrew/opt/protobuf/include)
""",
            )

            conan.tools.files.replace_in_file(
                self,
                "{0}/src/caffe/layers/hdf5_data_layer.cpp".format(self.source_folder),
                """#include <vector>""",
                """#include <algorithm>
#include <vector>
#include <random>
""",
            )
            conan.tools.files.replace_in_file(
                self,
                "{0}/src/caffe/layers/hdf5_data_layer.cpp".format(self.source_folder),
                '''#include "caffe/util/hdf5.hpp"''',
                """#include "caffe/util/hdf5.hpp"
static std::random_device rd;
static std::mt19937 g(rd());
""",
            )
            conan.tools.files.replace_in_file(
                self,
                "{0}/src/caffe/layers/hdf5_data_layer.cpp".format(self.source_folder),
                """std::random_shuffle(data_permutation_.begin(), data_permutation_.end());""",
                """std::shuffle(data_permutation_.begin(), data_permutation_.end(), g);""",
            )
            conan.tools.files.replace_in_file(
                self,
                "{0}/src/caffe/layers/hdf5_data_layer.cpp".format(self.source_folder),
                """std::random_shuffle(file_permutation_.begin(), file_permutation_.end());""",
                """std::shuffle(file_permutation_.begin(), file_permutation_.end(), g);""",
            )
            conan.tools.files.replace_in_file(
                self,
                "{0}/src/caffe/layers/hdf5_data_layer.cpp".format(self.source_folder),
                """std::random_shuffle(file_permutation_.begin(),
                              file_permutation_.end());""",
                """std::shuffle(file_permutation_.begin(),
                              file_permutation_.end(),
                              g);""",
            )
            conan.tools.files.replace_in_file(
                self,
                "{0}/src/caffe/layers/window_data_layer.cpp".format(self.source_folder),
                """CV_LOAD_IMAGE_COLOR""",
                """cv::IMREAD_COLOR""",
            )
            conan.tools.files.replace_in_file(
                self,
                "{0}/src/caffe/util/io.cpp".format(self.source_folder),
                """CV_LOAD_IMAGE_COLOR""",
                """cv::IMREAD_COLOR""",
            )
            conan.tools.files.replace_in_file(
                self,
                "{0}/src/caffe/util/io.cpp".format(self.source_folder),
                """CV_LOAD_IMAGE_GRAYSCALE""",
                """cv::IMREAD_GRAYSCALE""",
            )
            conan.tools.files.replace_in_file(
                self,
                "{0}/src/caffe/util/io.cpp".format(self.source_folder),
                """, 536870912""",
                """""",
            )
            conan.tools.files.replace_in_file(
                self,
                "{0}/CMakeLists.txt".format(self.source_folder),
                """add_subdirectory(src/gtest)""",
                """find_package(hdf5 REQUIRED)
find_package(libaec REQUIRED)
add_subdirectory(src/gtest)""",
            )
            conan.tools.files.replace_in_file(
                self,
                "{0}/src/caffe/CMakeLists.txt".format(self.source_folder),
                """target_link_libraries(caffe ${Caffe_LINKER_LIBS})""",
                """target_link_libraries(caffe ${Caffe_LINKER_LIBS} hdf5_hl-static hdf5_tools-static hdf5-static gflags glog::glog)""",
            )

        cmake.configure(variables=variables)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        cmake.install()
        fix_apple_shared_install_name(self)
