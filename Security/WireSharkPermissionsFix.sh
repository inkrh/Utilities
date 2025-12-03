echo "Changing /dev/bp* ownership to $(whoami):admin"
sudo chown $(whoami):admin /dev/bp*
ls -la /dev | grep bp


