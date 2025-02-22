#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

recipe_dir="$1"
shift

conan create "$recipe_dir" -pr:b=profiles/armv8_Macos_apple-clang_16 "$@"
