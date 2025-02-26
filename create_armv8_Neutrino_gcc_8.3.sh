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

export PATH=$QNX_HOST/usr/bin/:$PATH
export CHOST=ntoaarch64
export AR=ntoaarch64-ar
export AS=ntoaarch64-as
export CC=ntoaarch64-gcc
export CXX=ntoaarch64-g++
export LD=ntoaarch64-ld
export RANLIB=ntoaarch64-ranlib
export STRIP=ntoaarch64-strip

conan create "$recipe_dir" -pr:h=./profiles/armv8_Neutrino_gcc_8.3 -pr:b=default "$@"
