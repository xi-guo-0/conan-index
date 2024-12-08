from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get
import conan
import os

class grpcRecipe(ConanFile):
    name = "grpc"
    description = "An RPC library and framework"
    license = "Apache-2.0"
    generators = "CMakeDeps", "CMakeToolchain"
    no_copy_source = True
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "v1.68.2"
    url = "https://github.com/grpc/grpc/archive/refs/tags/{0}.tar.gz".format(version)

    def requirements(self):
        self.requires("c-ares/v1.34.3")
        self.requires("openssl/openssl-3.4.0")
        self.requires("protobuf/v29.1")
        self.requires("re2/2024-07-02")

    def source(self):
        get(self, self.url, strip_root=True)

    def configure_cmake(self):
        cmake = CMake(self)
        def convert_to_cmake_boolean(value):
            return "ON" if value else "OFF"

        variables = {}
        variables["BUILD_SHARED_LIBS"] = convert_to_cmake_boolean(self.options.shared)
        variables["BUILD_STATIC_LIBS"] = convert_to_cmake_boolean(not self.options.shared)
        variables["CMAKE_CXX_STANDARD"] = self.settings.compiler.cppstd
        variables["CMAKE_POSITION_INDEPENDENT_CODE"] = convert_to_cmake_boolean(True)

        variables["OpenSSL_DIR"] = os.path.join(self.dependencies["openssl"].package_folder, 'lib', 'cmake', 'OpenSSL')
        variables["Protobuf_DIR"] = os.path.join(self.dependencies["protobuf"].package_folder, 'lib', 'cmake', 'protobuf')
        variables["absl_DIR"] = os.path.join(self.dependencies["abseil-cpp"].package_folder, 'lib', 'cmake', 'absl')
        variables["c-ares_DIR"] = os.path.join(self.dependencies["c-ares"].package_folder, 'lib', 'cmake', 'c-ares')
        variables["gRPC_ABSL_PROVIDER"] = "package"
        variables["gRPC_CARES_PROVIDER"] = "package"
        variables["gRPC_PROTOBUF_PROVIDER"] = "package"
        variables["gRPC_RE2_PROVIDER"] = "package"
        variables["gRPC_SSL_PROVIDER"] = "package"
        variables["re2_DIR"] = os.path.join(self.dependencies["c-ares"].package_folder, 'lib', 'cmake', 're2')

        cmake.configure(variables=variables)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        cmake.install()
        fix_apple_shared_install_name(self)
