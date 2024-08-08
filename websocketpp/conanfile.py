from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.files import copy
from os.path import join

class websocketppRecipe(ConanFile):
    name = "websocketpp"
    description = "C++ websocket client/server library"
    license = "BSD-3-Clause license"
    version = "0.8.2"
    url = "https://github.com/zaphoyd/websocketpp.git"

    def source(self):
        git = Git(self)
        clone_args = ["--depth", "1", "--branch", self.version]
        git.clone(url=self.url, target=".", args=clone_args)

    def package(self):
        copy(self, "*", join(self.source_folder, "websocketpp"), join(self.package_folder, "include", "websocketpp"))
