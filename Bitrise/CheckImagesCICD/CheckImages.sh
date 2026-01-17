# Check images for particular keywords in source, sits in CICD pipeline after clone and after embedded assets are downloaded
# out == log report of detected keywords

# use case find keyword "merck" in common icons to identify potential brand leakage weak points across regions
# reporting only to provide recon information
# for future cases make this an input
# best results come after training, this is just a POC

KEYWORD="merck"

if [[ -z $(which tesseract) ]]; then
    echo "Leverages tesseract"
    echo "Try brew install tesseract"
    exit
fi

for f in $(find . -name "*.png" -o -name "*.jpeg" -o -name "*.jpg" -o -name "*.gif"); do
    echo "** Checking $f:"
    #for full visibility about what is being done
    #can be compacted
    RESULT=$(tesseract "$f" stdout)
    DISCOVERED=$(echo $RESULT | grep -i $KEYWORD)
    if [ -n "$DISCOVERED" ]; then
        echo "Found $KEYWORD: $DISCOVERED"
        #TODO: set flag and additional logic
    #TODO: else case if needed report file is clear
    fi
done
