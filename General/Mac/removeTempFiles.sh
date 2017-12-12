find $1 -name '._*' > todelete.txt

while read n; do rm "$n"; done < todelete.txt

echo "DONE"
