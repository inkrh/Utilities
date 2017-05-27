#!/bin/sh

#  LinodeBackup.sh
#  
#
#  Created by Robert Henden on 5/27/17.
#

@echo off
echo "WordpressBackup.sh <wordpress folder> <db user> <db password> <db name>"

##archive wordpress files

tar -czf WPBackup.tar "$0"


##dmup MySQL (insecure)
mysqldump -u $1 -p$2 $3 > sealevelsWP.sql

##tarball above archives
tar -czf SeaLevels.tar sealevelsWP.tar sealevelsWP.sql

##clean up
rm -rf sealevelsWP.tar
rm -rf sealevelsWP.sql


