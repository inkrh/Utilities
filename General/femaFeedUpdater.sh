curl -s https://www.fema.gov/api/open/v1/DisasterDeclarationsSummaries.json > femaEvents.json
python CleanFemaData.py
