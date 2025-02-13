#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

recipe_dir="$1"
shift

conan create "$recipe_dir" -pr:b=profiles/x86_64_Linux_gcc_11.4 "$@"
