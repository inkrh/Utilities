for f in *;
	do case "$f" in
		"$1")	echo "Skipping $f";;
		*) echo "Moving $f"; mv "$f" "$1/";;
esac
done

