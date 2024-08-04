import conan
from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps

class opencvRecipe(ConanFile):
    name = "opencv"
    description = "Open Source Computer Vision Library"
    license = "Apache-2.0 license"
    generators = "CMakeDeps", "CMakeToolchain"
    no_copy_source = True
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "with_ffmpeg": [True, False],
               "ANDROID_ABI": ["arm64-v8a"],
               "with_android_mediandk": [False, True],
               "with_android_native_camera": [False, True],
               "BUILD_opencv_dnn": [True, False]}
    default_options = {"shared": False,
                       "with_ffmpeg": False,
                       "ANDROID_ABI": "arm64-v8a",
                       "with_android_mediandk": False,
                       "with_android_native_camera": False,
                       "BUILD_opencv_dnn": True}
    version = "4.10.0"
    url = "https://github.com/opencv/opencv.git"

    def source(self):
        git = Git(self)
        git.clone(self.url, target=".", args=["--depth", "1", "--branch", self.version])
        conan.tools.files.replace_in_file(self, "cmake/OpenCVInstallLayout.cmake", '''if(ANDROID)

  ocv_update(OPENCV_BIN_INSTALL_PATH            "sdk/native/bin/${ANDROID_NDK_ABI_NAME}")
  ocv_update(OPENCV_TEST_INSTALL_PATH           "${OPENCV_BIN_INSTALL_PATH}")
  ocv_update(OPENCV_SAMPLES_BIN_INSTALL_PATH    "sdk/native/samples/${ANDROID_NDK_ABI_NAME}")
  ocv_update(OPENCV_LIB_INSTALL_PATH            "sdk/native/libs/${ANDROID_NDK_ABI_NAME}")
  ocv_update(OPENCV_LIB_ARCHIVE_INSTALL_PATH    "sdk/native/staticlibs/${ANDROID_NDK_ABI_NAME}")
  ocv_update(OPENCV_3P_LIB_INSTALL_PATH         "sdk/native/3rdparty/libs/${ANDROID_NDK_ABI_NAME}")
  ocv_update(OPENCV_CONFIG_INSTALL_PATH         "sdk/native/jni")
  ocv_update(OPENCV_INCLUDE_INSTALL_PATH        "sdk/native/jni/include")
  ocv_update(OPENCV_OTHER_INSTALL_PATH          "sdk/etc")''', '''if(ANDROID)

  ocv_update(OPENCV_BIN_INSTALL_PATH            "bin")
  ocv_update(OPENCV_TEST_INSTALL_PATH           "${OPENCV_BIN_INSTALL_PATH}")
  ocv_update(OPENCV_SAMPLES_BIN_INSTALL_PATH    "${OPENCV_BIN_INSTALL_PATH}")
  ocv_update(OPENCV_LIB_INSTALL_PATH            "${CMAKE_INSTALL_LIBDIR}")
  ocv_update(OPENCV_LIB_ARCHIVE_INSTALL_PATH    "${OPENCV_LIB_INSTALL_PATH}")
  ocv_update(OPENCV_3P_LIB_INSTALL_PATH         "${OPENCV_LIB_INSTALL_PATH}/opencv4/3rdparty")
  ocv_update(OPENCV_CONFIG_INSTALL_PATH         "${OPENCV_LIB_INSTALL_PATH}/cmake/opencv4")
  ocv_update(OPENCV_INCLUDE_INSTALL_PATH        "${CMAKE_INSTALL_INCLUDEDIR}/opencv4")
  ocv_update(OPENCV_OTHER_INSTALL_PATH          "${CMAKE_INSTALL_DATAROOTDIR}/opencv4")''')

    def requirements(self):
        if self.options.with_ffmpeg:
            self.requires("ffmpeg/n7.0.1")

    def configure_cmake(self):
        cmake = CMake(self)
        def convert_to_cmake_boolean(value):
            return "ON" if value else "OFF"
        variables = {}

        with_gtk = self.settings.arch == "x86_64" and self.settings.os == "Linux"

        variables["CMAKE_POSITION_INDEPENDENT_CODE"] = convert_to_cmake_boolean(True)
        if self.settings.os == "Android":
            variables["ANDROID_ABI"] = self.options.ANDROID_ABI
            variables["ANDROID_ABI"] = self.options.ANDROID_ABI
            variables["ANDROID_NATIVE_API_LEVEL"] = self.settings.os.api_level
            variables["BUILD_ANDROID_EXAMPLES"] = convert_to_cmake_boolean(False)
            variables["BUILD_ANDROID_PROJECTS"] = convert_to_cmake_boolean(False)
            variables["WITH_ANDROID_MEDIANDK"] = convert_to_cmake_boolean(self.options.with_android_mediandk)
            variables["WITH_ANDROID_NATIVE_CAMERA"] = convert_to_cmake_boolean(self.options.with_android_native_camera)

        variables["BUILD_DOCS"] = convert_to_cmake_boolean(False)
        variables["BUILD_EXAMPLES"] = convert_to_cmake_boolean(False)
        variables["BUILD_JASPER"] = convert_to_cmake_boolean(True)
        variables["BUILD_JAVA"] = convert_to_cmake_boolean(False)
        variables["BUILD_JPEG"] = convert_to_cmake_boolean(True)
        variables["BUILD_OPENEXR"] = convert_to_cmake_boolean(True)
        variables["BUILD_PERF_TESTS"] = convert_to_cmake_boolean(False)
        variables["BUILD_PNG"] = convert_to_cmake_boolean(True)
        variables["BUILD_SHARED_LIBS"] = convert_to_cmake_boolean(self.options.shared)
        variables["BUILD_STATIC_LIBS"] = convert_to_cmake_boolean(not self.options.shared)
        variables["BUILD_TBB"] = convert_to_cmake_boolean(True)
        variables["BUILD_TESTS"] = convert_to_cmake_boolean(False)
        variables["BUILD_TIFF"] = convert_to_cmake_boolean(True)
        variables["BUILD_ZLIB"] = convert_to_cmake_boolean(True)
        variables["BUILD_opencv_apps"] = convert_to_cmake_boolean(False)
        variables["BUILD_opencv_dnn"] = convert_to_cmake_boolean(self.options.BUILD_opencv_dnn)
        variables["BUILD_opencv_python2"] = convert_to_cmake_boolean(False)
        variables["BUILD_opencv_python3"] = convert_to_cmake_boolean(False)
        variables["CMAKE_CXX_STANDARD"] = self.settings.compiler.cppstd
        variables["ENABLE_NEON"] = convert_to_cmake_boolean(self.settings.arch == "armv8")
        variables["INSTALL_C_EXAMPLES"] = convert_to_cmake_boolean(False)
        variables["INSTALL_PYTHON_EXAMPLES"] = convert_to_cmake_boolean(False)
        variables["WITH_1394"] = convert_to_cmake_boolean(False)
        variables["WITH_CUDA"] = convert_to_cmake_boolean(False)
        variables["WITH_EIGEN"] = convert_to_cmake_boolean(False)
        variables["WITH_FFMPEG"] = convert_to_cmake_boolean(self.options.with_ffmpeg)
        variables["WITH_GDAL"] = convert_to_cmake_boolean(False)
        variables["WITH_GPHOTO2"] = convert_to_cmake_boolean(False)
        variables["WITH_GSTREAMER"] = convert_to_cmake_boolean(False)
        variables["WITH_GTK"] = convert_to_cmake_boolean(with_gtk)
        variables["WITH_GTK_2_X"] = convert_to_cmake_boolean(with_gtk)
        variables["WITH_IPP"] = convert_to_cmake_boolean(False)
        variables["WITH_JPEG"] = convert_to_cmake_boolean(True)
        variables["WITH_OPENEXR"] = convert_to_cmake_boolean(True)
        variables["WITH_PNG"] = convert_to_cmake_boolean(True)
        variables["WITH_QT"] = convert_to_cmake_boolean(False)
        variables["WITH_QUICKTIME"] = convert_to_cmake_boolean(False)
        variables["WITH_V4L"] = convert_to_cmake_boolean(True)
        variables["WITH_VTK"] = convert_to_cmake_boolean(False)
        variables["WITH_WEBP"] = convert_to_cmake_boolean(True)
        variables["WITH_XINE"] = convert_to_cmake_boolean(False)

        if self.options.with_ffmpeg:
            ffmpeg_root = self.dependencies["ffmpeg"].package_folder
            variables["FFMPEG_DIR"] = ffmpeg_root
            variables["OPENCV_FFMPEG_USE_FIND_PACKAGE"] = convert_to_cmake_boolean(True)
            variables["OPENCV_FFMPEG_SKIP_BUILD_CHECK"] = convert_to_cmake_boolean(True)
        cmake.configure(variables=variables)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        cmake.install()
