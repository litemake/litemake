# litemake

<!-- Badges -->
[![build](https://img.shields.io/github/workflow/status/litemake/litemake/%E2%9C%85%EF%B8%8F%20Test?logo=github)](https://github.com/litemake/litemake/actions/workflows/test.yaml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/litemake/litemake/master.svg)](https://results.pre-commit.ci/latest/github/litemake/litemake/master)
[![codecov](https://img.shields.io/codecov/c/github/litemake/litemake?logo=codecov)](https://codecov.io/gh/litemake/litemake)

<!-- Short description -->
A new way to build, test and distribute your C/C++ projects and libraries.

## What is litemake?

**litemake** is a cross-platform CLI that aims to simplify the building, testing and distribution process of your C/C++ code.

By configuration a simple `package.litemake.toml` file, **litemake** will be able to automatically:

- Download required dependencies and build you project
- Build only changed files to reduce compile time (similar to Make)
- Build and run your tests
- And more!

With additional (simple and short) configuration files like `settings.litemake.toml` and `package.litemake.toml` you will be able to publish your package or project, and make it avaliable to other users and developers.

## The vision behind litemake

There is a common phrase among the C/C++ developer community: *"(The convention) doesn't matter, just be consistent"* [^1]. I however, strongly believe that a good convention is one that allows the developer to implement whatever he wants, but also allows others easily understand the intensions of the former. A good convention won't limit the developer, but will guide him.

### Compering to other programming languages

Other programming languages (mostly high-level ones like *Python* or *JavaScript*), have established package managers, build systems, and other tools to distribute your code, all all of that as a part of the programming language itself. Those tools allow developers to publish and download, build or install their package/library/project using a single command. Furthermore, developers can use other dependencies in their projects, and use other tools to improve their development including testing environments for example.

### And what about C/C++?

**litemake** aims to bring the described above to the C/C++ community. By writing a simple configuration file `package.litemake.toml` and placing it in your project's root directory, users will be able to download all required dependencies, build and install your application just by using one command: `litemake`.

Furthermore, with tools like [nanotest] you will be able to automatically build and run your tests. The sky is really the limit!

## Supported compilers and platforms

Currently, supporting multiple platforms is not our main focus. **Litemake**
is mainly designed for the Linux operation system and the Gnu compiler
collection (GCC, G++). However, **litemake** is not designed to work *only* on
Linux with those compilers, and thus it works on Windows, MacOS and with the
Clang compiler family. That means that it is possible to run litemake with
those compilers and on those systems, however you may encounter some errors
and it is not recommended.

<!-- Links -->

[^1]: https://api.csswg.org/bikeshed/?force=1&url=https://raw.githubusercontent.com/vector-of-bool/pitchfork/develop/data/spec.bs#intro
