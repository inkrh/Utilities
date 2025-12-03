echo "Removing __MACOSX folders from all zip files in path: $1"
find "$1" -type f -name '*.zip' -exec zip -d '{}' __MACOSX/\* \;

