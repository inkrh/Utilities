for x in {0..512};
do for y in {0..512};
do siege -c 10 -r 10 $0/tiles/$x/$y/9 > test.png;
done;
done;


