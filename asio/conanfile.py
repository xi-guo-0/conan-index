from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.files import copy
from os.path import join

class asioRecipe(ConanFile):
    name = "asio"
    description = "Asio C++ Library"
    license = "Boost Software License"
    version = "asio-1-28-0"
    url = "https://github.com/chriskohlhoff/asio.git"

    def source(self):
        git = Git(self)
        clone_args = ["--depth", "1", "--branch", self.version]
        git.clone(url=self.url, target=".", args=clone_args)

    def package(self):
        copy(self, "*", join(self.source_folder, "asio", "include"), join(self.package_folder, "include"))
