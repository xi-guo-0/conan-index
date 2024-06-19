#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

recipe_dir="$1"
shift

conan create "$recipe_dir" -pr:b=profiles/armv8_Android_34 "$@"
