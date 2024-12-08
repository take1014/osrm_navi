import folium
from requester import OSRMRequester

if __name__ == '__main__':
    # start_lonlat = [139.767125, 35.681236] # Tokyo
    # end_lonlat   = [135.503869, 34.687317] # Osaka
    # start_lonlat = [142.3650, 43.7687] # Asahikawa
    start_lonlat = [139.3816, 36.2962] # Gunma-ken Subaru-cho
    end_lonlat   = [130.5611, 31.5611] # Kagoshima

    hosts_url = '192.168.3.45:5000'

    # create instance
    osrm_requester = OSRMRequester(hosts_url=hosts_url)
    # set start, end
    osrm_requester.setStartLonLat(lon_lat=start_lonlat)
    osrm_requester.setEndLonLat(lon_lat=end_lonlat)
    # request query
    osrm_requester.requestRoute()
    # print TBT
    tbt_list = osrm_requester.getTBT()
    print(tbt_list)

    # get route
    result = osrm_requester.getRoute()
    route = result["routes"][0]
    list_locations = []
    for leg in route["legs"]:
        for step in leg["steps"]:
            maneuver = step["maneuver"]
            for it in step['intersections']:
                list_locations.append(it['location'][::-1])

    # save map
    m = folium.Map()
    folium.Marker(location=start_lonlat, icon=folium.Icon(color='red')).add_to(m)
    folium.Marker(location=end_lonlat[::-1]).add_to(m)
    m.fit_bounds(list_locations)
    line = folium.vector_layers.PolyLine(locations=list_locations, color='blue', weight=10)
    line.add_to(m)
    m.save("map.html")
