#!/usr/bin/python3

from pb import apple_pb2
import requests
from urllib3.exceptions import InsecureRequestWarning

#suppress certificate warnings for hitting Apple's location services API endpoint
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def build_request(bssid: str) -> bytes:
    req = apple_pb2.AppleReq()
    wifi = req.wifis.add()
    wifi.mac = bssid

    req.noise = 0
    # Get 20 results
    req.limit = 20

    return req.SerializeToString()


def get_lat_long_from_apple(bssid):
    '''
    @brief: using Apple location services API, gets the co-ordinates
    @param: bssid: the BSSID to attempt to geolocate
    @returns: (lat,lonig) tuple of floats

    Note - Paper by François-Xavier Aguessy and Côme Demoustier
    http://fxaguessy.fr/rapport-pfe-interception-ssl-analyse-donnees-localisation-smartphones/
    '''

    #data_bssid = f"\x12\x13\n\x11{bssid}\x18\x00\x20\01"
    headers = {'Content-Type':'application/x-www-form-urlencoded',
                'Accept':'*/*',
                "Accept-Charset": "utf-8",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language":"en-us",
                'User-Agent':'locationd/1753.17 CFNetwork/711.1.12 Darwin/14.0.0'
                }

    # Get proto format request paylaod
    payload = build_request(bssid)

    # Wrap in Apple’s request envelope
    header = b"\x00\x01\x00\x05en_US\x00\x13com.apple.locationd\x00\x0a8.1.12B411\x00\x00\x00\x01\x00\x00\x00"
    data = header + bytes([len(payload)]) + payload

    resp = requests.post('https://gs-loc.apple.com/clls/wloc',
                         headers=headers,
                         data=data,
                         verify=False
           )

    if resp.status_code != 200:
        raise RuntimeError(f"Request failed: {response.status_code}")

    bssidResponse = apple_pb2.AppleResp()
    bssidResponse.ParseFromString(resp.content[10:]) # Skip HTTP2 header

    for wifi in bssidResponse.wifi:
        #Skip any BSSIDs Apple returns that aren't the one we requested
        #Need to normalize each MAC byte because the string representation will
        #strip out leading 0s for some reason. So for e.g., need to turn
        # 0:11:aa:bb:cc:dd
        # into 00:11:aa:bb:cc:dd
        checkBSSID = ":".join("0" + x if len(x) == 1 else x for x in
                wifi.bssid.split(":"))
        if checkBSSID != bssid:
            continue
        lat = wifi.location.lat * pow(10,-8)
        long = wifi.location.lon * pow(10,-8)

        return lat, long

    return -180.0, -180.0

if __name__ == "__main__":
    bssid = '18:4b:0d:0b:1c:dc'
    lat, long = get_lat_long_from_apple(bssid)
    print(f"Lat, Long for {bssid} = {lat, long}")

