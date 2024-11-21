import conan
from conan import ConanFile
from conan.tools.files import get
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps

class chibiSchemeRecipe(ConanFile):
    name = "chibi-scheme"
    description = "Minimal Scheme Implementation for use as an Extension Language"
    license = "BSD 3-clause"
    generators = "CMakeDeps", "CMakeToolchain"
    no_copy_source = True
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "ANDROID_ABI": ["arm64-v8a"]}
    default_options = {"shared": False,
                       "ANDROID_ABI": "arm64-v8a"}
    version = "0.11"
    url = "https://github.com/ashinn/chibi-scheme/archive/refs/tags/{0}.zip".format(version)

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

        cmake.configure(variables=variables)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        cmake.install()
