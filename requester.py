#!/usr/bin/env python3
import json
import requests

class OSRMRequester:
    def __init__(self, hosts_url:str):
        self.__hosts_url = hosts_url
        self.__start_lonlat = None
        self.__end_lonlat   = None
        self.__route = None

    def setStartLonLat(self, lon_lat:list) -> None:
        assert len(lon_lat) == 2
        self.__start_lonlat = lon_lat

    def setEndLonLat(self, lon_lat:list) -> None:
        assert len(lon_lat) == 2
        self.__end_lonlat = lon_lat

    def requestRoute(self) -> None:
        assert self.__start_lonlat != None and self.__end_lonlat != None
        query = f"http://{self.__hosts_url}/route/v1/driving/{self.__start_lonlat[0]},{self.__start_lonlat[1]};{self.__end_lonlat[0]},{self.__end_lonlat[1]}?overview=full&geometries=geojson&steps=true"
        # query = f"http://{self.__hosts_url}/route/v1/driving/{self.__start_lonlat[0]},{self.__start_lonlat[1]};{self.__end_lonlat[0]},{self.__end_lonlat[1]}?overview=full&geometries=polyline&steps=true"
        response = requests.get(query)
        self.__route = response.json()

    def getRoute(self) -> None:
        return self.__route

    def getTBT(self):
        route = self.__route["routes"][0]
        tbt_list = []
        for leg in route["legs"]:
            for step in leg["steps"]:
                maneuver = step["maneuver"]
                tbt_list.append({
                    "tbt": f"{maneuver['type']} {maneuver.get('modifier', '')}",
                    "location":maneuver['location'],
                    "distance_meter": step['distance'],
                    "duration_sec":step['duration'],
                    "road_name": step['name']
                })
        return tbt_list

    def saveRoute(self, filename='./route.json') -> None:
        assert self.__route != None
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.__route, f, ensure_ascii=False, indent=2)
