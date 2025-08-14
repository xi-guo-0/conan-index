from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import get

# Recommend using NDK r27 or above


class onnxruntimeRecipe(ConanFile):
    name = "onnxruntime"
    description = "Open standard for machine learning interoperability"
    license = "Apache-2.0"
    generators = "CMakeDeps", "CMakeToolchain"
    no_copy_source = True
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "use_qnn": [True, False],
        "build_qnn_ep_static_lib": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "use_qnn": False,
        "build_qnn_ep_static_lib": False,
    }
    version = "v1.22.1"
    url = f"https://github.com/microsoft/onnxruntime/archive/refs/tags/{version}.zip"

    def source(self):
        get(self, self.url, strip_root=True)

    def configure_cmake(self):
        cmake = CMake(self)

        def convert_to_cmake_boolean(value):
            return "ON" if value else "OFF"

        variables = {
            "BUILD_SHARED_LIBS": convert_to_cmake_boolean(self.options.shared),
            "BUILD_STATIC_LIBS": convert_to_cmake_boolean(not self.options.shared),
            "CMAKE_CXX_STANDARD": self.settings.compiler.cppstd,
            "CMAKE_POSITION_INDEPENDENT_CODE": convert_to_cmake_boolean(
                self.options.get_safe("fPIC", True)
            ),
            "ONNX_BUILD_SHARED_LIB": convert_to_cmake_boolean(self.options.shared),
            "CMAKE_CXX_FLAGS_INIT": "-Wno-unused-function",
        }

        if self.options.use_qnn:
            variables["onnxruntime_USE_QNN"] = "ON"
            variables["onnxruntime_QNN_HOME"] = "/opt/qcom/aistack/qairt/2.30.0.250109"
            variables["onnxruntime_BUILD_QNN_EP_STATIC_LIB"] = convert_to_cmake_boolean(
                self.options.build_qnn_ep_static_lib
            )

        cmake.configure(source_folder="cmake", variables=variables)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        cmake.install()
        fix_apple_shared_install_name(self)
