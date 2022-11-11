from io import StringIO
import sys

from conan import ConanFile
from conan.tools.files import copy
from conan.tools.scm import Git
from conan.errors import ConanException


class Skia(ConanFile):
    name = "skia"
    version = "main"
    license = "BSD 3-Clause"
    url = "https://github.com/ModernCircuits/conan-skia.git"
    description = "A 2D/3D Vector rendering engine"
    topics = ("render", "vector", "2d", "3d")
    settings = "os", "compiler", "build_type", "arch"

    # @property
    # def _python_executable(self):
    #     exe = sys.executable
    #     return str(exe).replace("\\", "/")

    # def layout(self):
    #     self.folders.source = "."

    def source(self):
        git = Git(self)
        clone_args = ['--depth', '1', '--branch', self.version]
        git.clone(url="https://github.com/google/skia.git", args=clone_args)

    def build_requirements(self):
        self.tool_requires("gn/cci.20210429")

    def build(self):
        opts = [
            "is_official_build=true",

            "skia_enable_fontmgr_empty=true",
            "skia_enable_gpu=true",
            "skia_enable_pdf=false",
            "skia_use_expat=false",
            "skia_use_freetype=false",
            "skia_use_harfbuzz=false",
            "skia_use_icu=false",
            "skia_use_libjpeg_turbo_decode=false",
            "skia_use_libjpeg_turbo_encode=false",
            "skia_use_libpng_decode=false",
            "skia_use_libpng_encode=false",
            "skia_use_libwebp_decode=false",
            "skia_use_libwebp_encode=false",
            "skia_use_vulkan=false",
            "skia_use_wuffs=false",
            "skia_use_zlib=false",
            # "clang_win=\"C:\Program Files\LLVM\"",
            # "extra_cflags=[\"/arch:AVX\"]",
        ]

        if self.settings.build_type == "Debug":
            opts += ["is_debug=true"]
        else:
            opts += ["is_debug=false"]

        if len(opts) > 0:
            opts = '"--args=%s"' % " ".join(opts)
        else:
            opts = ""

        self.output.info("gn options: %s" % (opts))

        cwd = f'{self.source_folder}/skia'
        # self.run('python tools/git-sync-deps', cwd=cwd)
        self.run('gn.exe gen out/conan-build %s ' % (opts), cwd=cwd)
        self.run('ninja -C out/conan-build', cwd=cwd)

        # build() will have access to the sources, obtained with the clone in source()
        # hello = os.path.join(self.source_folder, "src/hello.cpp")
        # self.output.info("MYCMAKE-BUILD: {}".format(load(self, cmake)))
        # self.output.info("MYFILE-BUILD: {}".format(load(self, hello)))

# "skia_use_libjpeg_turbo_decode=false",
# "skia_use_libjpeg_turbo_encode=false",
# "skia_use_libwebp_decode=false",
# "skia_use_libwebp_encode=false",
# "skia_use_system_harfbuzz=false",
# "skia_use_system_icu=false",
# "skia_use_system_expat=false",
# "skia_enable_pdf=false",
# "skia_use_system_libpng=false",
# "skia_use_system_zlib=false"