# Conan Skia

Work in progress...

## Windows

```sh
conan create . demo/testing --keep-source -pr:h=default -pr:b=default
# or
conan create . demo/testing --keep-source -pr:h=clang-cl -pr:b=clang-cl
```

```ini
; profile: default
[settings]
os=Windows
os_build=Windows
arch=x86_64
arch_build=x86_64
build_type=Release
compiler=Visual Studio
compiler.version=17
compiler.runtime=MD

[options]
[build_requires]
[env]

[conf]
tools.cmake.cmaketoolchain:generator=Ninja
```

```ini
; profile: clang-cl
[settings]
os=Windows
os_build=Windows
arch=x86_64
arch_build=x86_64
build_type=Release
compiler=Visual Studio
compiler.version=17
compiler.toolset=ClangCL
compiler.runtime=MD

[options]

[build_requires]

[env]

[conf]
tools.cmake.cmaketoolchain:generator=Visual Studio 17 2022
```

### Issues

- [ ] ClangCL does not work yet, because escaping the LLVM root path causes errors with `gn` on powershell or cmd
