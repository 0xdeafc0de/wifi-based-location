# WiFi based location
Geolocates Wi-Fi BSSIDs (MAC addresses) using Apple’s private location API - https://gs-loc.apple.com/clls/wloc

It returns approximate latitude and longitude coordinates if Apple has location data associated with the BSSID.

## Disclaimer

This tool accesses undocumented Apple APIs. Use responsibly and **only for educational or research purposes**. Do not abuse this service.

## Background

This implementation is inspired by:

- [iSniff-GPS](https://github.com/hubert3/iSniff-GPS/tree/master/iSniff_GPS)
- Research by François-Xavier Aguessy and Côme Demoustier  
  ([PDF Link](http://fxaguessy.fr/rapport-pfe-interception-ssl-analyse-donnees-localisation-smartphones/))

## Requirements
- Python 3.7+
- `protobuf` library (preferably v3.20.x)
- `requests` library
- `protoc` protobuf compiler
```bash
pip install requests protobuf==3.20.*
```

### Usage
The pb/apple.proto file defines the Request and Response messages. The `protoc` generated python code is avaialbe.
If you need to regenerate the code use protoc as below

``` bash
protoc --python_out=. apple.proto
```

To get the Lat, Long of a location, find out the BSSID from the nearest AP (e.g. Your Home WiFI AP) and pass it as below -

```python
lat, long = get_lat_long_from_apple("XX:XX:XX:XX:1c:dc")
print(f"Lat: {lat}, Long: {long}")
```
## Output
```bash
Lat, Long for XX:XX:XX:XX:1c:dc = (13.02603054, 77.7641983)
```
