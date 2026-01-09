#relies on factor and imagemagick
#TODO: handling to check they exist on system

# file names
RAW_FILE="rawpixels.rgb"
OUTPUT_FILE="image.png"
GPG_FILE="TempFile.gpg"
TMP_BINARY_NUMBERS="TempBinary.txt"

#Infile > gpg > binary (means we can have error correction) > hex for image > image
#Symmetric for now - should be fine

gpg -o "$GPG_FILE" -c $1

#Convert to binary
xxd -b "$GPG_FILE" | sed -e 's/^.*: //; s/[[:space:]][[:space:]]*.\{6,6\}$//' > "$TMP_BINARY_NUMBERS"

#TODO: merge these to remove TempBinary.txt handle in memory
#perl -pe 'print pack("B8", $_)' < TempBinary.txt > TempBinary.bin

fileContent=$(cat "$TMP_BINARY_NUMBERS")
cleanedFileContent=$(echo "$fileContent" | tr -d '[:space:]')

contentlength="${#fileContent}"
cleanedFileContentLength="${#cleanedFileContent}"

#echo $contentlength
echo $cleanedFileContentLength
echo "****"
#echo ${fileContent}
echo "****"
echo ${cleanedFileContent}


#populate as hex bytes for clarity in coding (possible to go from binary -> binary but we want to be sure)
#padding from binary to black/white pixel with 3 channels (1==FFFFFF, 0==000000, if there is any other color on reading it back then something went wrong, but should be able to recover from it using that padding i.e. FFFF27==1)
#TODO: I don't know what I was thinking here, so should drink coffee and rethink this logic
outputHex=""
for ((i = 0; i < cleanedFileContentLength; i++)); do
    char=${cleanedFileContent:$i:1}
    hexValue="FFFFFF"
    if [ "$char" -eq "0" ]; then
        hexValue="000000"
    fi
    outputHex=$outputHex$hexValue
done

#calculate size
echo $outputHex
outputHexLength="${#outputHex}"
echo $outputHexLength
hexLength=$(((outputHexLength / 3)/2))
echo $hexLength

#TODO: Calculate the middle factor and error handling/padding
#Calculate the smallest factor
smallest_factor=$(factor $hexLength | cut -d: -f2 | cut -d' ' -f2)
# Calculate the largest factor (not including number 1 or n)
largest_factor=$((hexLength / smallest_factor))
echo $smallest_factor
echo $largest_factor
expected=$(( smallest_factor*largest_factor*3 ))
echo "Expected $expected"


echo "$outputHex" | xxd -r -p > "$RAW_FILE"
actual=$(wc -c < "$RAW_FILE")
echo "Actual $actual"

magick convert -size "${smallest_factor}x${largest_factor}" -depth 8 RGB:"$RAW_FILE" "$OUTPUT_FILE"
