#!/bin/sh
echo "$0"
echo ALC address "$1"
echo ftp user "$2"
echo ftp address "$4"
echo ftp folder "$5"
telnet $1
expect "login:"
send "root"
expect "Password:"
send ""
cd /mnt/sd/VideoPlayback;
for f in *.avi;
do 
  ftpput -v -u "$2" -p "$3" "$4" "$5""$f" "$f"
done

##use ./TransferVideosFromALCCamera.sh ALC user pass ftpserver destfolder
##use sudo -s launchctl load -w /System/Library/LaunchDaemons/ftp.plist
##to start an ftp server on localhost

##e.g. ./TransferVideosFromALCCamera.sh 10.0.1.20 ftpUser ftpPass 10.0.1.1 /Volumes/Storage/ 
