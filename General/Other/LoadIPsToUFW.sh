#!/bin/sh

#  LoadIPsToUFW.sh
#  
#
#  Created by Robert Henden on 10/25/17.
#
# relies on ufw / fail2ban
# apt-get install fail2ban

echo "Looking for failed authentication attempts, saving output to authFailures.txt"

cat /var/log/auth.log | grep Failed > authFailures.txt

echo "Stripping out IPs, saving output to troubleIPs.txt"

grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' authFailures.txt > troubleIPs.txt

echo "Feeding each entry into UFW (NB duplicates are to be expected and handled by UFW"

while read IPADDR; do ufw deny from $IPADDR; done < troubleIPs.txt

echo "DONE"

