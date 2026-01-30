if [[ -z $(which mitmproxy) ]]; then
	echo "mitmproxy not installed"
	echo "Trying brew install mitmproxy"
	brew install mitmproxy
fi

if [[ -z $(which mitmproxy) ]]; then
	echo "Not installed"
	exit
fi

echo "On device Settings > Wifi > Info on Current connection"
echo "Set device proxy to $(ipconfig getifaddr en0):8080"

echo "Starting mitmproxy in new Terminal window"
osascript -e 'tell app "Terminal" to do script "mitmproxy; read"'

echo "Visit http://mitm.it on device to install certificates for https traffic"

