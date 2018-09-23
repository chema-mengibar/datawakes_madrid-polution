    [...]
    # .......................................................................... block-test: Check the location of stations in map
    #com: Add stations-postalcodes and -region_id to dataframe
    buffer_postalcode = []
    buffer_region = []

    for idStation, station in df_stations.iterrows():
        pc = -1
        rid = -1
        _lon =  station["lon"]
        _lat =  station["lat"]
        stationCursor = mapservice.mapCoorToXY( ( _lon, _lat ) )
        for idr, region in enumerate( mapservice.xyPoligons ):
            if len( region["data"]) > 2:
                if mapservice.isPointInPolygon( stationCursor , region["data"] ):
                    pc = region["meta"]["postalcode"]
                    rid = idr
        buffer_postalcode.append( pc  )
        buffer_region.append( rid )

    df_stations['postalcode'] = buffer_postalcode
    df_stations['region_id'] = buffer_region




----------


    gradient1 = _dwg.defs.add( _dwg.linearGradient() )
    # define the gradient from red to white
    gradient1.add_stop_color(0, _colors.white).add_stop_color(1,  _colors.contrast.blue).add_stop_color(2,  _colors.contrast.orange).add_stop_color(3,  _colors.contrast.rosa)
    # use gradient for filling the rect
    _dwg.add(_dwg.rect((10,10), (50,200), fill=gradient1.get_paint_server()))
