#!/bin/bash

SOURCEINPUT=$1
SOURCEFOLDER=$1
IFS=$'\n'

#is input location an ipa/apk/aab or a folder?
REGEXSTRING='(.ipa)|(.aab)|(.apk)'

#check for required utilities
echo 'Checking required tools'

if [[ -z $(which otfinfo) ]]; then
    echo "TTF and OTF Analysis requires otfinfo"
    echo "Try brew install lcdf-typetools"
    exit
fi

if [[ -z $(which woff2_decompress) ]]; then
    echo "OPTIONAL WOFF2 support requires woff2_decompress"
    echo "brew tap bramstein/webfonttools && brew install woff2"
fi

if [[ -z $(which  woff2otf) ]]; then
    echo "OPTIONAL WOFF support requires woff2otf"
    echo "git clone https://github.com/hanikesn/woff2otf.git"
    echo "Then move woff2otf.py to binaries folder as woff2otf"
fi


echo "Checking App Bundles For OTF/TTF Fonts..."
#if ipa/apk/aab extract to tmp folder
if [[ -z "$SOURCEINPUT" ]]; then
    echo "No source location specified"
    echo "Usage $0 <ipa|aab|apk|folder/*.ipa|folder/*.aab|folder/*.apk>"
    exit
fi

if [[ "$SOURCEINPUT" =~ $REGEXSTRING ]]; then
    echo "Checking assets in app bundle at $SOURCEINPUT extracting to ./tmp"
    unzip -q "$SOURCEINPUT" -d tmp
    SOURCEFOLDER="tmp"
fi

# looking for woff/woff2
WOFF=$(find "$SOURCEFOLDER" -name "*.woff")
WOFF2=$(find "$SOURCEFOLDER" -name "*.woff2")

# convert to ttf (woff2) or otf (woff) in situ? separate folder and maintain reference?
if [ -n "$WOFF" ]; then
    echo "** WOFF file paths in $SOURCEINPUT **"
    echo "Attempting conversion to otf"
    for f in $WOFF; do
        echo "Converting $f to ${f%.}.otf"
        woff2otf "$f" "${f%.}.otf"
    done
fi

if [ -n "$WOFF2" ]; then
    echo "** WOFF2 file paths in $SOURCEINPUT **"
    echo "Attempting conversion to ttf"
    for f in $WOFF2; do
        echo "Converting $f to ${f%.}.ttf"
        woff2_decompress "$f"
    done
fi

echo "Any files successfully converted to TTF or OTF will reflect in results below"
echo "Not all files follow the same formats so errors are possible"

#run find in folder and output results to STD out
# looking for otf/ttf
OTF=$(find "$SOURCEFOLDER" -name "*.otf")
TTF=$(find "$SOURCEFOLDER" -name "*.ttf")

if [ -n "$OTF" ]; then
    echo " ** OTF file paths in $SOURCEINPUT **"
#    echo ${OTF//tmp\//} | tr " " "\n"
    echo ${OTF//tmp\//}
    echo "** Actual font names **"
    for f in $OTF; do
        echo "$f"
        otfinfo -p "$f"
        otfinfo -i "$f"
    done
fi

if [ -n "$TTF" ]; then
    echo "** TTF file paths in $SOURCEINPUT **"
    echo ${TTF//tmp\//}
    echo "** Actual font names **"
    for f in $TTF; do
        echo "$f"
        otfinfo -p "$f"
        otfinfo -i "$f"

    done
fi

#if ipa/apk/aab remove tmp folder
if [[ "$SOURCEINPUT" =~ $REGEXSTRING ]]; then
    rm -rf tmp
fi


