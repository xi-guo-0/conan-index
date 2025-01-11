from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get
import conan
import os


class libjson_rpc_cppRecipe(ConanFile):
    name = "libjson-rpc-cpp"
    description = "C++ framework for json-rpc (json remote procedure call)"
    license = "MIT"
    generators = "CMakeDeps", "CMakeToolchain"
    no_copy_source = True
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "v1.4.1"
    url = "https://github.com/cinemast/libjson-rpc-cpp/archive/refs/tags/{0}.tar.gz".format(
        version
    )

    def requirements(self):
        self.requires("argtable2/argtable2-13")
        self.requires("hiredis/v1.2.0")
        self.requires("jsoncpp/1.9.6")

    def source(self):
        get(self, self.url, strip_root=True)

    def configure_cmake(self):
        cmake = CMake(self)

        if int(str(self.settings.compiler.cppstd)) >= 20:
            conan.tools.files.replace_in_file(
                self,
                "{0}/src/jsonrpccpp/server/threadpool.h".format(self.source_folder),
                "typename std::result_of<F(Args...)>::type",
                "typename std::invoke_result<F, Args...>::type",
            )
        conan.tools.files.replace_in_file(
            self,
            "{0}/src/jsonrpccpp/CMakeLists.txt".format(self.source_folder),
            "target_link_libraries(common jsoncpp_lib_static)",
            "target_link_libraries(common ${JSONCPP_LIBRARY})",
        )

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

        variables["COMPILE_EXAMPLES"] = convert_to_cmake_boolean(False)
        variables["COMPILE_TESTS"] = convert_to_cmake_boolean(False)

        argtable2 = self.dependencies["argtable2"].package_folder
        hiredis = self.dependencies["hiredis"].package_folder
        jsoncpp = self.dependencies["jsoncpp"].package_folder

        variables["CMAKE_PREFIX_PATH"] = "{0};{1};{2}".format(
            argtable2, hiredis, jsoncpp
        )
        variables["ARGTABLE_INCLUDE_DIR"] = os.path.join(argtable2, "include")
        variables["ARGTABLE_LIBRARY"] = os.path.join(argtable2, "lib", "libargtable2.a")
        variables["HIREDIS_INCLUDE_DIR"] = os.path.join(hiredis, "include")
        variables["HIREDIS_INCLUDE_DIRS"] = os.path.join(hiredis, "include")
        variables["HIREDIS_LIBRARY"] = os.path.join(hiredis, "lib", "libhiredis.a")
        variables["JSONCPP_INCLUDE_PREFIX"] = os.path.join(jsoncpp, "include", "json")
        variables["JSONCPP_LIBRARY"] = os.path.join(jsoncpp, "lib", "libjsoncpp.a")

        cmake.configure(variables=variables)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        cmake.install()
        fix_apple_shared_install_name(self)
