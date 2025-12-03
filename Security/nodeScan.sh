#!/bin/bash 
oldPWD="$PWD"
echo "Scanning folder $1"
cd $1
echo "**RUNNING npm audit**"
if hash npm 2>/dev/null; then
	npm audit
else
	echo "npm not found - please install node - see https://nodejs.org/"
fi
echo "**RUNNING retire**"
if hash retire 2>/dev/null; then
	retire
else
	echo "retire not found - please install retire using  npm install -g retire"
fi
echo "**searching for strings in non-binary files as indicators of weak points**"
keywords=("SELECT\s" "DELETE\s" "INSERT\s"  "REPLACE\s" "SQL"  "POST"  "SOAP" "SQL" "SERVER" "MONGODB"  "DATABASE"  "CREATE"  "TABLE"  "VALUES"  "PREPARE"  "FTP" "HTTP://"  "SERIALIZE"  "INSTALL"  "PASSWORD"  "USER"  "RECEIVER"  "PROVIDER"  "AUTHORIZATION"  "CERTIFICATE"  "LEAKAGE"  "SESSION"  "INJECTION"  "EXPIRATION" "CSP"  "FTP"  "CERT"  "SESS"  "REALM"  "EXEC("  "SOCKET"  "RAND(" "RND"  "RANDOM" "ENCRYPT"  "INSECURE", "TODO")

for keyword in "${keywords[@]}"; do
    echo ">Keyword -  $keyword"
    grep -r  -n -F -I -i --exclude-dir=node_modules $keyword $1
done
cd "$oldPWD"
