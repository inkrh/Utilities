#image > convert FF to 1 / 00 to 0 > binary > gpg file > gpg decrypt > Outfile

RAW_FILE="image.raw"
HEX_DUMP="hexdump.txt"
OUTPUT_GPG="output_file.gpg"
OUTPUT_PLAINTEXT="output.txt"
#get hex dump
magick convert "$1" -depth 8 rgb:- | cat > "$RAW_FILE"

xxd -p "$RAW_FILE" > "$HEX_DUMP"

fileContent=$(cat "$HEX_DUMP"  | tr -d '\n' )

echo "Hex dump"
echo $fileContent

#iterate over hex dump to convert back to binary, should be 6 character chunks of either ffffff==1 or 000000==0
outputBinary=""
#TODO: Error handling
for (( i=0; i<${#fileContent}; i+=6 )); do
    chunk="${fileContent:i:6}"
    
    if [ "$chunk" = "ffffff" ]; then
        bo="1"
    elif [ "$chunk" = "000000" ]; then
        bo="0"
    else
        echo "Something went wrong here, this is where error handling will go"
    #plan is to approximate the extremes
    fi
    outputBinary=$outputBinary$bo
done

outputHex=""
for (( i=0; i<${#outputBinary}; i+=64 )); do
    chunk="${outputBinary:i:64}"
    outputHex=$outputHex$(echo "obase=16; ibase=2; $chunk" | bc)
done

echo "$outputHex" | xxd -r -p > "$OUTPUT_GPG"

gpg -o "$OUTPUT_PLAINTEXT" -d "$OUTPUT_GPG"
