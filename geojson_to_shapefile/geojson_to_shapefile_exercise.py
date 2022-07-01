#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json 

from osgeo import ogr, gdal


def create_polygon(coords):
    ring = ogr.Geometry(ogr.wkbLinearRing)
    for coord in coords:
        for xy in coord:
            ring.AddPoint(xy[0],xy[1])
            poly = ogr.Geometry(ogr.wkbPolygon)
            poly.AddGeometry(ring)
    return poly.ExportToIsoWkt()

def create_shp_with_geojson(json,geo_type):
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF-8")
    driver = ogr.GetDriverByName("ESRI Shapefile")
    properties_temp=list(json['features'][0]['properties'])
    
    if geo_type=='Polygon' or geo_type=='MultiPolygon':
        #修改的地方
    elif geo_type=='Point': #建立shapefile的檔案名稱,屬性表格格式
        #修改的地方
    elif geo_type == 'LineString':
        #修改的地方
            
    for record in json['features']:
        geo = record.get("geometry")
        geo_type = geo.get('type')
        #print(geo)
        temp=list(record['properties'])
        
        if geo_type == 'Polygon':
            #修改的地方
            
        elif geo_type == 'MultiPolygon':
            #修改的地方
            
        elif geo_type == 'Point':
            #修改的地方
            
                
        elif geo_type == 'LineString':
            #修改的地方
            
        else:
            print('Could not discern geometry')
with open("/root/groundwater_address/地下水觀測井位置圖_彰化縣現存站.json",'r', encoding="UTF-8") as jsonfile: #讀取json檔案
    data = json.load(jsonfile)
    geo_type=str(data['features'][0]['geometry']['type'])
    temp=list(data['features'][0]['properties'])
    #print(temp)
    create_shp_with_geojson(data,geo_type)

