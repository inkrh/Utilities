#!/usr/bin/env bash
# fail if any commands fails
set -e
# make pipelines' return status equal the last command to exit with a non-zero status, or zero if all commands exit successfully
set -o pipefail
# debug log
set -x

#assumptions - running on CICD server with su access

#https://learn.microsoft.com/en-us/dotnet/maui/ios/deployment/publish-cli?view=net-maui-10.0#define-build-properties-in-your-project-file

#signing inputs normally expected to have been set in csproj file
#alternative in build environment if not set
#this script just assumes if  $BITRISE_PROVISION_URL and $BITRISE_CODE_SIGN_IDENTITY not set don't sign

#Expected example
#Codesign key "Apple Distribution: John Smith (AY2GDE9QM7)"
#Path to provisioning profile "RelativePath/To/ProvisionURL.mobileprovision"

#also should set .net targetframework(s) - e.g. net8.0-ios, net10.0-ios, net8.0-android as environment variable to make reusable but I'm being lazy
#should really set output folder as a variable being lazy here because this is just my memory aid

OUTPUTFOLDER="./dist"

if [[ -z $(which dotnet) ]]; then
    echo "Requires dotnet CLI"
    echo "Running brew install --cask dotnet-sdk"
    brew install --cask dotnet-sdk
    #official method
    #    brew install wget
    #    wget https://dot.net/v1/dotnet-install.sh
    #    chmod +x dotnet-install.sh
    #    ./dotnet-install.sh
fi


#because I like to see it in the output
echo $(dotnet --version)

#install .Net MAUI workload
echo "Installing .Net MAUI workload"
dotnet workload install maui --source https://api.nuget.org/v3/index.json

#build ios
#if succeeds will be in $OUTPUTFOLDER/<SOLUTIONNAME>.ipa
# documentation at https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-build

if [[ -z "$BITRISE_CODE_SIGN_IDENTITY" || -z "$BITRISE_PROVISION_URL" ]]; then
#build without signing, I can always resign the ipa later
    dotnet build -f net10.0-ios -c Release -p:BuildIpa=true -p:RuntimeIdentifier=ios-arm64 -p:EnableCodeSigning=false -p:BuildIpa=true -o $OUTPUTFOLDER
else
        dotnet build -f net10.0-ios -c Release -p:BuildIpa=true -p:RuntimeIdentifier=ios-arm64 -p:EnableCodeSigning=true -p:ArchiveOnBuild=true -p:BuildIpa=true -p:CodesignKey=$BITRISE_CODE_SIGN_IDENTITY -p:CodesignProvision=$BITRISE_PROVISION_URL -o $OUTPUTFOLDER
fi

#because I like making sure what is there in logs, is already in dotnet build output
find "$OUTPUTFOLDER" -name "*.ipa"

cp "$OUTPUTFOLDER/*.ipa" "$BITRISE_DEPLOY_DIR/"
