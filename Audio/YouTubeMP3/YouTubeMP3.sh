if [ -z "$1" ]
  then
    echo "Missing URL(s)"
    echo "Syntax:"
    echo "YouTubeMP3.sh <YouTube URL>" 
  else
    echo "Grabbing YouTube URLs and saving them as mp3s"
    for var in "$@"
      do
        echo "STARTING $var"
        youtube-dl --extract-audio --audio-format mp3 "$var"
        echo "$var DONE"
    done
fi
