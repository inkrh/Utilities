#!/usr/bin/env bash
# fail if any commands fails
set -e
# make pipelines' return status equal the last command to exit with a non-zero status, or zero if all commands exit successfully
set -o pipefail
# debug log
set -x

# Check file was downloaded
if ! test -f "$DOWNLOADED_IOS_FILE"; then
    echo "ipa wasn't found in expected place"
    exit 1
fi

if [[ -z "$DOWNLOADED_IOS_FILE" ]]; then
    echo "DOWNLOADED_IOS_FILE wasn't set"
    exit 1
fi


#download profile file


STATUS_CODE=$(curl -sw '%{http_code}' "$BITRISE_PROVISION_URL" -o "newProfile.mobileprovision")

#status logging
if [ "$STATUS_CODE" != "200" ]; then
    echo "❌ Download of provisioning profile failed with $STATUS_CODE status code."
    exit 1
fi

export NEW_PROVISION="newProfile.mobileprovision" 

echo "Resigning ipa"
echo "Required:"
echo "DOWNLOADED_IOS_FILE: $DOWNLOADED_IOS_FILE"
echo "NEW_DEVELOPER (team ID): $NEW_DEVELOPER"
echo "NEW_BUNDLE: $NEW_BUNDLE"
echo "Optional:"
echo "NEW_VERSION_NUMBER: $NEW_VERSION_NUMBER"
echo "NEW_BUILD_NUMBER: $NEW_BUILD_NUMBER"


echo "Checking $DOWNLOADED_IOS_FILE"

# unzip it
unzip -qo "$DOWNLOADED_IOS_FILE" -d extracted
# discover any frameworks/appex/etc submodules and create a list to feed to that section
find -d extracted  \( -name "*.app" -o -name "*.appex" -o -name "*.framework" -o -name "*.dylib" \) > directories.txt
#Define payload folder
PAYLOAD_DIR="$(ls extracted/Payload/)"

if [[ -z "$NEW_BUNDLE" ]]; then
    echo "NEW_BUNDLE was empty"
    exit 1
fi

echo "Changing BundleID to : $NEW_BUNDLE"
/usr/libexec/PlistBuddy -c "Set:CFBundleIdentifier $NEW_BUNDLE" "extracted/Payload/$PAYLOAD_DIR/Info.plist"

        
#check existing version number
renum='^[0-9]+$'
version=$(/usr/libexec/PlistBuddy -c "Print :CFBundleShortVersionString" "extracted/Payload/$PAYLOAD_DIR/Info.plist")
echo "Existing version number is $version"

#change version number, keep for later use
if [[ -z "$NEW_VERSION_NUMBER" ]]; then
    echo "NEW_VERSION_NUMBER was empty not changing version number"
    newVersion=$version
else
    newVersion=$NEW_VERSION_NUMBER
    /usr/libexec/PlistBuddy -c "Set:CFBundleShortVersionString $newVersion" "extracted/Payload/$PAYLOAD_DIR/Info.plist"
fi




if [[ -z "$NEW_BUILD_NUMBER" ]]; then
    echo "NEW_BUILD_NUMBER was empty not changing build number"
else
    echo "Setting build # to $NEW_BUILD_NUMBER"
    /usr/libexec/PlistBuddy -c "Set:CFBundleVersion $NEW_BUILD_NUMBER" "extracted/Payload/$PAYLOAD_DIR/Info.plist"
fi

#Uncomment to set min OS verson
#/usr/libexec/PlistBuddy -c "Set:MinimumOSVersion 15.0" "extracted/Payload/$PAYLOAD_DIR/Info.plist"


if [ -f "extracted/Payload/$PAYLOAD_DIR/embedded.mobileprovision" ]; then
    # get the original entitlements
    echo "Original Entitlements"
    security cms -D -i "extracted/Payload/$PAYLOAD_DIR/embedded.mobileprovision" > t_entitlements_fullOLD.plist
    /usr/libexec/PlistBuddy -x -c 'Print:Entitlements' t_entitlements_fullOLD.plist > t_entitlementsOLD.plist
    # list them for output
    cat t_entitlementsOLD.plist
else
    echo "No original signing found"
fi

# resigning work
echo "Working with: $NEW_DEVELOPER"
# copy new provisioning profile under new developer certificate
cp "$NEW_PROVISION" "extracted/Payload/$PAYLOAD_DIR/embedded.mobileprovision"

echo "New Entitlements"
# get the new entitlements
security cms -D -i "$NEW_PROVISION" > t_entitlements_full.plist
/usr/libexec/PlistBuddy -x -c 'Print:Entitlements' t_entitlements_full.plist > t_entitlements.plist
# list them for output
cat t_entitlements.plist


while IFS='"'; read -ra SIGNING_ARRAY; do
    for i in "${SIGNING_ARRAY[@]}"; do
        if [[ $i == *"$NEWDEVELOPER"* ]]; then
            echo "Found signing identity  $i"
            CERTIFICATE=$i
        fi
    done
done <<< $(security find-identity -v -p codesigning | grep $NEW_DEVELOPER)

FRAMEWORKS_DIR="extracted/Payload/$PAYLOAD_DIR/Frameworks"

if [ -d "$FRAMEWORKS_DIR" ]; then
        if [ "$NEW_DEVELOPER" == "" ]; then
            error "ERROR: embedded frameworks detected, re-signing applications without a team identifier does not work"
        fi

        echo "Resigning embedded frameworks using certificate: $CERTIFICATE"
        for framework in "$FRAMEWORKS_DIR"/*
        do
            if [[ "$framework" == *.framework || "$framework" == *.dylib ]]; then
                echo "Resigning $framework"
                /usr/bin/codesign --verbose --generate-entitlement-der -f -s "$CERTIFICATE" "$framework"
            else
                echo "Ignoring non-framework: $framework"
            fi
        done
    fi

/usr/bin/codesign --verbose --generate-entitlement-der -f -s "$CERTIFICATE"  --entitlements "t_entitlements.plist" "extracted/Payload/$PAYLOAD_DIR"

#zip up new content
echo "Creating the re-signed IPA"
cd extracted
zip -qry ../$NEW_BUNDLE.ipa *
cd ..
cp $NEW_BUNDLE.ipa "$BITRISE_DEPLOY_DIR/"

echo "Cleaning up temp files"
# clean up local files
rm -rf extracted
rm -rf *.plist
rm -rf directories.txt
        
echo "DONE"




