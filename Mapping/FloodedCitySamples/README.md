AirqualityTileServer.py

  *Fetches air quality index tiles from WAQI, operates timed cache to avoid over-hitting original service and represents.*



CountyLocationLookup.db

femaEvents.json

femaFeedUpdater.sh

FEMA.db

cleanFema.json

CleanFemaData.py

  *Fetches FEMA data, cleans it to make it usable, then adds new content to FEMA.db.*



full8.tiff

CreateSourceTiles.py

  *Builds global elevation data set*



LandslideEndpoint.sh

landslides.json

  *Fetches global landslide data*



nasaEvents.json

nasaFeedUpdater.sh

  *Fetches NASA warnings*



combinedPOI.db

POIServer.py

  *Presents POI created from WWF and the above NASA/landslide data*




quiz.py

quizDB.db

  *Environmental based quiz data*



tileServerTester.sh

  *Siege testing script for flooded.city's tile server*
