#!/bin/bash
AABPATH=$1
KEYSTOREPATH=$2
KEYSTOREPASS=$3
KEYSTOREALIAS=$4
KEYSTOREALIASPASS=$5

MISSING="FALSE"

echo "Output aab will be the same as input aab (mutates signing on source aab)"

#check for JAVA_HOME and other requirements
if [[ -z "$JAVA_HOME" ]]; then
    echo "Requires JDK and JAVA_HOME to be set"
    MISSING="TRUE"
fi

if [[ -z "$AABPATH" ]]; then
    echo "Missing path to AAB"
    MISSING="TRUE"
fi

if [[ -z "$KEYSTOREPATH" ]]; then
    echo "Missing path to keystore"
    MISSING="TRUE"
fi

if [[ -z "$KEYSTOREPASS" ]]; then
    echo "Missing keystore password"
    MISSING="TRUE"
fi

if [[ -z "$KEYSTOREALIAS" ]]; then
    echo "Missing alias"
    MISSING="TRUE"
fi

if [[ -z "$KEYSTOREALIASPASS" ]]; then
    echo "No alias password set, assuming same as keystore"
fi

if [[ $MISSING == "TRUE" ]]; then
    echo "Usage $0 <AAB path> <keystore path> <keystore password> <alias> <optional alias password>"
    exit
fi

#at this point should have aab path, keystore path, keystore password, alias, and possibly alias password

#remove old signing
zip -d "$AABPATH" META-INF/\*

if [[ -z "$KEYSTOREALIASPASS" ]]; then
    #sign with new keystore
    "$JAVA_HOME/bin/jarsigner" -verbose -sigalg SHA256withRSA -digestalg SHA-256 -keystore  "$KEYSTOREPATH" -storepass $KEYSTOREPASS "$AABPATH" "$KEYSTOREALIAS"
else
    "$JAVA_HOME/bin/jarsigner" -verbose -sigalg SHA256withRSA -digestalg SHA-256 -keystore  "$KEYSTOREPATH" -storepass $KEYSTOREPASS -keypass $KEYSTOREALIASPASS "$AABPATH" "$KEYSTOREALIAS"
fi


