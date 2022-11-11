#!/bin/sh

cd /c/skia
echo "Building skia"

./bin/gn gen out/Static --args='is_official_build=true skia_use_libjpeg_turbo_decode=false skia_use_libjpeg_turbo_encode=false skia_use_libwebp_decode=false skia_use_libwebp_encode=false skia_use_system_harfbuzz=false skia_use_system_icu=false  skia_use_system_expat=false skia_enable_pdf=false skia_use_system_libpng=false skia_use_system_zlib=false clang_win="C:\Program Files\LLVM" extra_cflags=["/arch:AVX"]'

ninja -C out/Static

# ./bin/gn gen out/ClangCL_MinSize --args='is_official_build=true skia_enable_optimize_size=true skia_use_libjpeg_turbo_decode=false skia_use_libjpeg_turbo_encode=false skia_use_libwebp_decode=false skia_use_libwebp_encode=false skia_use_system_harfbuzz=false skia_use_system_icu=false skia_use_system_libpng=false skia_use_system_expat=false skia_enable_pdf=false clang_win="C:\Program Files\LLVM" extra_cflags=["/arch:AVX"]'

# ninja -C out/ClangCL_MinSize