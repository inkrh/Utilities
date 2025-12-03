#!/bin/sh

#  WordpressBackup.sh
#  
#
#  Created by Robert Henden on 5/27/17.
#

@echo off
echo "WordpressBackup.sh <wordpress folder> <db user> <db password> <db name>"

##archive wordpress files

tar -czf WPBackup.tar "$0"


##dmup MySQL (insecure)
mysqldump -u $1 -p$2 $3 > WP.sql

##tarball above archives
tar -czf Backup.tar WPBackup.tar WP.sql

##clean up
rm -rf WPBackup.tar
rm -rf WP.sql


