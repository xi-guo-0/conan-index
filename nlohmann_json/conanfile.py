from conan import ConanFile
from conan.tools.files import download
from conan.tools.files import copy
from os.path import join

class nlohmann_jsonRecipe(ConanFile):
    name = "nlohmann_json"
    description = "JSON for Modern C++"
    license = "MIT License"
    version = "v3.11.3"
    url = "https://github.com/nlohmann/json/releases/download/{}/json.hpp".format(version)

    def source(self):
        download(self, self.url, "json.hpp")

    def package(self):
        copy(self, "json.hpp", self.source_folder, join(self.package_folder, "include", "nlohmann"))
