#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

recipe_dir="$1"
shift

if [ -z "$QNX_HOST" ]; then
    echo "QNX_HOST is undefined"
    exit 1
fi

if [ -z "$$QNX_TARGET" ]; then
    echo "QNX_TARGET is undefined"
    exit 1
fi

export TARGET=ntoaarch64
export AR=$TARGET-ar
export AS=$TARGET-as
export CC=$TARGET-gcc
export CHOST=$TARGET
export CXX=$TARGET-g++
export LD=$TARGET-ld
export RANLIB=$TARGET-ranlib
export STRIP=$TARGET-strip

CUR_DIR=$(realpath -- "$( dirname -- "$0" )" )
export CONAN_CMAKE_TOOLCHAIN_FILE="$CUR_DIR/toolchains/aarch64_qnx.toolchain.cmake"

conan create "$recipe_dir" -pr:h=./profiles/armv8_QNX_gcc_5.4 -pr:b=default "$@"
