# !/bin/bash
SOURCEFOLDER=$1
NEWPROVISION=$2
NEWCERTSHA=$3
DEVELOPER=$4
BUNDLE=$5
VERSIONSUFFIX=$6
NEWNAME=$7
APPEXPROV=$8

#./IntuneResignAndWrapNameChange.sh "<PathToProvisioningProfile>" "<Cert SHA>" "<Cert name>" "<Bundle ID>" "<Versioning>" "<New name>"

echo "Wildcard Wrapping"
echo "Syntax: $0 IPA_FOLDER NEW_PROFILE NEW_CERTSHA NEW_DEVELOPER BUNDLE NEW_VERSIONSUFFIX NEW_NAME SUBMODULE_PROFILE"
echo ""
echo "Using: $SOURCEFOLDER $NEWPROVISION $NEWCERTSHA $DEVELOPER $BUNDLE $VERSIONSUFFIX $NEWNAME $APPEXPROV"

if [[ -z "$APPEXPROV" ]]; then
    APPEXPROV=$NEWPROVISION
    echo "SUBMODULE_PROFILE was empty, using $APPEXPROV"
fi

# read all ipas in SOURCEFOLDER
find -d "$SOURCEFOLDER" -type f -name "*.ipa" > files.txt
# feed them each to resigning/wrapping
while IFS='' read -r ipas || [[ -n "$ipas" ]]; do
        echo "Checking $ipas"
        # copy each to tools operating folder
        cp "$ipas" original.ipa
        # unzip it
        unzip -qo original.ipa -d extracted
        # discover any frameworks/appex/etc submodules and create a list to feed to that section
        find -d extracted  \( -name "*.app" -o -name "*.appex" -o -name "*.framework" -o -name "*.dylib" \) > directories.txt

        # entitlements work
        APPLICATION="$(ls extracted/Payload/)"
        
        #get original bundle ID last element
        echo "Getting old bundle ID"
        bundleID=$(/usr/libexec/PlistBuddy -c "Print :CFBundleIdentifier" "extracted/Payload/$APPLICATION/Info.plist")
        echo "$bundleID"
        IFS="." read -r -a array <<< "$bundleID"
        
        # set bundleID (for group folders wildcard)
        BUNDLE=${BUNDLE/"*"/${array[${#array[@]}-1]}}
        unset array
        echo "$BUNDLE"
        echo "Changing BundleID to : $BUNDLE"
        /usr/libexec/PlistBuddy -c "Set:CFBundleIdentifier $BUNDLE" "extracted/Payload/$APPLICATION/Info.plist"
        
        #set name
        if [[ -z "$NEWNAME" ]]; then
        echo "Setting App Name to : $NEWNAME"
        /usr/libexec/PlistBuddy -c "Set:CFBundleDisplayName $NEWNAME" "extracted/Payload/$APPLICATION/Info.plist"
        else
            echo "Retaining old App Name"
            NEWNAME=$(/usr/libexec/PlistBuddy -c "Print :CFBundleDisplayName" "extracted/Payload/$APPLICATION/Info.plist")
            echo "$NEWNAME"
        fi
        
        #add to version number
        renum='^[0-9]+$'
        version=$(/usr/libexec/PlistBuddy -c "Print :CFBundleShortVersionString" "extracted/Payload/$APPLICATION/Info.plist")
            
        if [[ $VERSIONSUFFIX =~ $renum ]]
        then
            echo "Adding .$VERSIONSUFFIX to BundleShortVersionString"
            newVersion="$version.$VERSIONSUFFIX"
            echo "Setting to $newVersion"
        elif [[ $VERSIONSUFFIX = "RESET" ]]
        then
            newVersion="1.0"
            echo "Resetting version number to 1.0"
        elif [[ $VERSIONSUFFIX = "+" ]]
        then
            echo "Incrementing version number"
            newVersion=$(echo $version | gawk -F"." '{$NF+=1}{print $0RT}' OFS="." ORS="")
        elif [[ $VERSIONSUFFIX != "" ]]
        then
            echo "Setting version to $VERSIONSUFFIX"
            newVersion=$VERSIONSUFFIX
        else
            echo "Not adding version suffix or changing in plist"
            newVersion=$version
            
        fi
        /usr/libexec/PlistBuddy -c "Set:CFBundleShortVersionString $newVersion" "extracted/Payload/$APPLICATION/Info.plist"
        
        # get the original entitlements
        echo "Original Entitlements"
        security cms -D -i "extracted/Payload/$APPLICATION/embedded.mobileprovision" > t_entitlements_fullOLD.plist
        /usr/libexec/PlistBuddy -x -c 'Print:Entitlements' t_entitlements_fullOLD.plist > t_entitlementsOLD.plist
        # list them for output
        cat t_entitlementsOLD.plist

        # resiging work
        echo "Resigning with certificate: $DEVELOPER"
        # copy new provisioning profile under new developer certificate
        cp "$NEWPROVISION" "extracted/Payload/$APPLICATION/embedded.mobileprovision"
        echo "New Entitlements"
        # get the new entitlements
        security cms -D -i "$NEWPROVISION" > t_entitlements_full.plist
        /usr/libexec/PlistBuddy -x -c 'Print:Entitlements' t_entitlements_full.plist > t_entitlements.plist
        # list them for output
        cat t_entitlements.plist

        #resign submodules using list previously generated - NB I originally forgot to specify the separate APPEXPROV here
        while IFS='' read -r submodule || [[ -n "$submodule" ]]; do
            echo "Working: $submodule"
            if [[ "$submodule" == *".appex" ]]; then
            #copy new appex provisioning profile
               cp "$APPEXPROV" "$submodule/embedded.mobileprovision"
               security cms -D -i "$submodule/embedded.mobileprovision" > t_entitlements_appex.plist
               /usr/libexec/PlistBuddy -x -c 'Print:Entitlements' t_entitlements_appex.plist > t_appex_entitlements.plist
               #sign appex
               /usr/bin/codesign --continue -f -s "$DEVELOPER" --entitlements "t_appex_entitlements.plist" "$submodule"
            # just resign other stuff
            else
            /usr/bin/codesign --continue -f -s "$DEVELOPER" --entitlements "t_entitlements.plist"  "$submodule"
            fi
        done < directories.txt

        #zip up new content
        echo "Creating the Signed IPA"
        cd extracted
        zip -qry ../extracted.ipa *
        cd ..
        cp extracted.ipa "${ipas%.ipa}${newVersion}NotWrapped.ipa"
        #wrap new ipa using InTune tool (must be from dmg as provided, at /Volumes/InTuneMAMAppPackager) and output to original folder
        echo "Wrapping"
        newFileName="${ipas%.ipa}${newVersion}Wrapped.ipa"
        # /Volumes/IntuneMAMAppPackager/InTuneMAMPackager/Contents/MacOS/IntuneMAMPackager -i /<path of input app>/<app filename> -o /<path to output folder>/<app filename> -p /<path to provisioning profile> -c <SHA1 hash of the certificate> [-b [<output app build string>]] [-v] [-e] [-x /<array of extension provisioning profile paths>]
        /Volumes/IntuneMAMAppPackager/IntuneMAMPackager/Contents/MacOS/IntuneMAMPackager -i extracted.ipa -o "$newFileName" -p $NEWPROVISION -c "$NEWCERTSHA" -v true
        echo "Wrapped ipa is at $newFileName"
        echo "New bundle ID is $BUNDLE"
        echo "Cleaning up temp files"
        # clean up local files
        rm -rf extracted
        rm -rf *.ipa
        rm -rf *.plist
        rm -rf directories.txt
        echo "NEXT"
done < files.txt
rm -rf files.txt
echo "DONE"
