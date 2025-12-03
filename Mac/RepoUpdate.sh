for f in */;
do
	cd "$f";
	if [ -d ".git" ]; then
		echo "Pulling latest in $f";
		git pull;
	fi
	cd ..;
done

