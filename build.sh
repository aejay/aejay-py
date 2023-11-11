#!/bin/zsh

# Populate all the .spec files in the directories under the current one:
PACKAGE_SPECS=$(find . -name '*.spec')

# Print them out:
echo "Found package specs:"
for spec in $PACKAGE_SPECS; do
    echo "  $spec"
done

# Build the packages. These are pyinstaller specs, so we just need to move into
# the directory and run pyinstaller for the spec:

for spec in $PACKAGE_SPECS; do
    echo "Building $spec"
    cd $(dirname $spec)
    poetry run pyinstaller $(basename $spec) --noconfirm
    cd -
done

