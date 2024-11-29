#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

recipe_dir="$1"
shift

if [ -z "$ANDROID_NDK" ]; then
    echo "ANDROID_NDK is undefined"
    exit 1
fi

SOURCE_PROPERTIES="$ANDROID_NDK/source.properties"
if [ ! -f "$SOURCE_PROPERTIES" ]; then
    echo "source.properties file does not exist."
    exit 1
fi

NDK_VERSION=$(awk -F "=" '/Pkg.Revision/ {print $2}' "$SOURCE_PROPERTIES" | tr -d '[:space:]')

if ! [[ $NDK_VERSION =~ ^[0-9]+(\.[0-9]+)*$ ]]; then
    echo "Invalid NDK version format: $NDK_VERSION"
    exit 1
fi

IFS='.' read -ra VERSION_NUMBERS <<< "$NDK_VERSION"

if [ "${VERSION_NUMBERS[0]}" -ge 18 ]; then
    echo "NDK version is greater than or equal to r18: $NDK_VERSION"
else
    echo "NDK version is less than r18: $NDK_VERSION"
    exit 1
fi

OS="$(uname -s)"
case "$OS" in
  Linux*)     TOOLCHAIN=$ANDROID_NDK/toolchains/llvm/prebuilt/linux-x86_64/bin;;
  Darwin*)    TOOLCHAIN=$ANDROID_NDK/toolchains/llvm/prebuilt/darwin-x86_64/bin;;
  *)          echo "Unknown operating system: $OS" >&2; exit 1;;
esac
export TARGET=aarch64-linux-android
export API=30
export AR=$TOOLCHAIN/llvm-ar
export CC=$TOOLCHAIN/$TARGET$API-clang
export AS=$CC
export CXX=$TOOLCHAIN/$TARGET$API-clang++
export LD=$TOOLCHAIN/ld
export RANLIB=$TOOLCHAIN/llvm-ranlib
export STRIP=$TOOLCHAIN/llvm-strip

conan create "$recipe_dir" -pr:h=./profiles/armv8_Android_api30 -pr:b=default "$@"
