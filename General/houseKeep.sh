sudo periodic daily weekly monthly
find ~/Projects -iname "._*" -exec rm -rf {} \;
find ~/Documents -iname "._*" -exec rm -rf {} \;
find ~/Projects -iname ".DS*" -exec rm -rf {} \;
find ~/Documents -iname ".DS*" -exec rm -rf {} \;

