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

conan create "$recipe_dir" -pr:b=profiles/armv8_Android_34 "$@"
