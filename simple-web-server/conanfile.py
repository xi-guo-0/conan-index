from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get

class simple_web_serverRecipe(ConanFile):
    name = "simple-web-server"
    description = "A very simple, fast, multithreaded, platform independent HTTP and HTTPS server and client library implemented using C++11 and Boost.Asio. Created to be an easy way to make REST resources available from C++ applications"
    license = "MIT"
    generators = "CMakeDeps", "CMakeToolchain"
    no_copy_source = True
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    version = "v3.1.1"
    url = "https://gitlab.com/eidheim/Simple-Web-Server/-/archive/{0}/Simple-Web-Server-{0}.tar.gz".format(version)

    def requirements(self):
        self.requires("asio/asio-1-32-0")

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
        variables["CMAKE_POSITION_INDEPENDENT_CODE"] = convert_to_cmake_boolean(self.options.fPIC)

        variables["CMAKE_PREFIX_PATH"] = self.dependencies["openssl"].package_folder
        variables["PKG_CONFIG_PATH"] = self.dependencies["asio"].package_folder

        cmake.configure(variables=variables)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        cmake.install()
