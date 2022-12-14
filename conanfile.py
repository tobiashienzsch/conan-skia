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

    @property
    def _gn(self):
        if self.settings.os == "Windows":
            return "gn.exe"
        return "gn"

    # def layout(self):
    #     self.folders.source = "."

    def source(self):
        git = Git(self)
        clone_args = ['--depth', '1', '--branch', self.version]
        git.clone(url="https://github.com/google/skia.git", args=clone_args)

    def build_requirements(self):
        self.tool_requires("gn/cci.20210429")

    def build(self):
        is_debug_build = "false"
        if self.settings.build_type == "Debug":
            is_debug_build = "true"

        opts = [
            f"is_debug={is_debug_build}",
            "is_official_build=true",

            "skia_enable_fontmgr_empty=true",
            "skia_enable_gpu=true",
            "skia_enable_graphite=false",
            "skia_enable_pdf=false",
            "skia_enable_optimize_size=true",
            "skia_enable_skottie=false",

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
        ]

        if self.settings.os == "Windows":
            opts.append("skia_enable_fontmgr_win=true")
            # opts.append('''extra_cflags=["/arch:AVX"]''')
            # "clang_win=\"C:\Program Files\LLVM\"",

        if self.settings.os == "Macos":
            opts.append("skia_use_gl=false")
            opts.append("skia_use_metal=true")
            # opts.append('''extra_cflags=["-flto=full"]''')
            # opts.append('''extra_ldflags=["-flto=full"]''')

        assert len(opts) > 0

        args = " ".join(opts)
        gn_args = f'"--args={args}"'
        self.output.info("raw options: %s" % (args))
        self.output.info("gn options: %s" % (gn_args))

        cwd = f'{self.source_folder}/skia'
        self.run(f'{self._gn} gen out/conan-build {gn_args} ', cwd=cwd)
        self.run('ninja -C out/conan-build', cwd=cwd)

    def package(self):
        src = f'{self.source_folder}/skia'
        out = f'{src}/out/conan-build'

        self.copy("*.h", dst="include/include",
                  src=f'{src}/include', keep_path=True)

        self.copy("*.lib", dst="lib", src=out, keep_path=False)
        self.copy("*.dll", dst="bin", src=out, keep_path=False)

        self.copy("*.a", dst="lib", src=out, keep_path=False)
        self.copy("*.so", dst="lib", src=out, keep_path=False)
        self.copy("*.dylib", dst="lib", src=out, keep_path=False)


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
