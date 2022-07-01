import geopandas as gpd
import pandas as pd #引用pandas套件進行數據分析
import os
import shapely.geometry
import json
import twd97
import csv
from geojson import Feature, Point, FeatureCollection, LineString, Polygon
import shapefile 
file=r"C:\Users\timchen\Desktop\notu class\專題\濁水溪shape file\高鐵站\A190010076V005.shp" #shapefile檔案路徑
gdf_Rail=gpd.read_file('{}'.format(file),decoding='utf-8')
#print (gdf_Rail)
counter=len(gdf_Rail)
temp=list(gdf_Rail)
point=0
for i in range(0,counter):
    jsonArray=[]
    record={}
    my_point=0
    counter=0
shp1=[]
gps_shp=[]
entries = os.listdir(r"C:\Users\timchen\Desktop\notu class\專題\濁水溪shape file\GNSS")
for i in range (0,len(entries)): #當i介於0~entries的長度時
    temp="" 
    for y in range (len(entries[i])-4,len(entries[i])):#當y介於entries-4~entries的長度時
        temp=temp+entries[i][y]#temp就會=最後四個字元
    if temp=='.shp':#若那四字源是.csv的話
        shp1.append(entries[i])#就找出是csv檔的標題,然後在後面附加上.csv
print(shp1) #印出shp1

for i in range(0,len(shp1)): #當i介於0~csv1的長度時
    word_temp=""
    for y in range(0,len(shp1[i])):#當y介於0~csv1[i]的長度時
        if(shp1[i][y])!='.':
            word_temp=word_temp+shp1[i][y]#沒讀到.就一個個讀入
        else:
            break#讀到.就跳出迴圈
    gps_shp.append(word_temp)#附加word_temp
#print(gps_shp) #第一步驟正確


for i in range(0,1):
    jsonArray = [] 
    temp1=[]
    total=[]
    templst=[]
for a in range(0,len(shp1)):
    word=shp1[a]
    gdf_Rail=gpd.read_file(r"C:\Users\timchen\Desktop\notu class\專題\濁水溪shape file\GNSS\{}".format(word),decoding='utf-8', newline='')            
    #print(shpReader)
    #print(gdf_Rail.iloc[5])
    for row in gdf_Rail: #add this python dict to json array
        templst.append(row)
        for row_json in range(len(gdf_Rail)):
            jsonArray.append(gdf_Rail.iloc[row_json])

    for y in range(0,len(jsonArray)):#當y介於0~jsonArray的長度時
         for z in range(0,len(templst)):#z介於0~temp的長度時(讀欄位名稱)
            #print(jsonArray[y]['{}'.format(templst[z])])
            #print(templst[z])
            try :
                if jsonArray[y]['{}'.format(templst[z])]=='' or jsonArray[y]['{}'.format(templst[z])]==' ':
                    del jsonArray[y]['{}'.format(templst[z])]
                else:
                    temp1.append(templst[z])
            except : 
                pass #否則,資料不為空就要附加上去
            
    total.append(temp1) 
for i in range(0,len(shp1)):
    counter1=[]
    counter2=[]
    counter3=[]
    new_json=[]
    
    geojson = {
        'type': 'FeatureCollection',
        'features': []
    }
    geojson1 = {
        'type': 'FeatureCollection',
        'features': []
    } #參考NKS_Week_WNES_20200207.json這份文件

    for y in range(0,len(total)): 
        counter=0
        for z in range(0,len(total[y])):
            
            if str(total[y-1][z][0])>'A' or str(total[y-1][z][0])<'Z': 
                #if str(total[y][z][0])>='0' and str(total[y][z][0])<='9': #判斷是否是數字字串 
                    #jsonArray[y][str(total[y][z])]=float(jsonArray[y][str(total[y][z])])#是的話轉成float
                if str(total[y][z])=='LocationBy' or str(total[y][z])=='Location_1': #判斷完整的經緯度
                    counter=counter+1
                    if type(jsonArray[y][str(total[y-1][z])])  != float :
                        jsonArray[y][str(total[y-1][z])]=float(jsonArray[y][str(total[y-1][z])])#是的話轉成float
                    if counter==2: #當累加到2也就是說x.y各存一筆
                        counter1.append(2)#append 2讓程式能跑if counter1[a]==2這個判斷式
                        counter2.append(y)#讓底下的程式可以知道是哪一筆有經緯度
                        counter3.append(z)
                        counter = 0 
                    else:
                        counter1.append(0)
    
    a=0
    b=0
    c=0
    for record in jsonArray:
        #print(jsonArray[counter2[b]]["LocationBy"])
        #print(record)
        if (counter1[a]==2 ):
            try : 
                temp1, temp2 = float(jsonArray[b]["LocationBy"]), float(jsonArray[b]['Location_1']) # LocationByTWD97_X:X , LocationByTWD97_Y:Y
                if   jsonArray[b]["Groundwate"] != "null" :
                    Groundwate = str(jsonArray[b]["Groundwate"])
                else :
                    Groundwate = ""
                if   jsonArray[b]["TownIdenti"] != "null" :
                    TownIdenti = str(jsonArray[b]["TownIdenti"])
                else :
                    TownIdenti = ""    
                    
                temp1, temp2 = twd97.towgs84(temp1, temp2)#呼叫一個能轉換座標系統的專用js
                my_point = Point((float(temp2), float(temp1)))#在圖像的特定點上繪製一個點((float(temp2), float(temp1)))
                b=b+1
                geojson['features'].append({
                'type': 'Feature',
                'geometry': my_point,
                'properties':{                              
                              'prop1':{
                                  "Address" : record['Address']  , "DisuseDate" : record['DisuseDate']  ,
                                  "Establishe" : record['Establishe']  ,"Establis_1" : record['Establis_1'] ,
                                  "Groundwate" : Groundwate , 
                              } , 
                              'prop2':{
                                  "Management" : record['Management'] , "Monitoring" : record['Monitoring'] ,
                                  "StationIde" : record['StationIde'] ,"StationNam" : record['StationNam'] ,
                                  "Status" : record['Status'] , "TownIdenti" : TownIdenti ,
                              } 
                              
                             } ,  
            })
            except  : 
                pass
                
        else:
            geojson1['features'].append({
            'type': 'Feature',
            'properties': record,
        }) #參考NKS_Week_WNES_20200207.json這份文件格式
            c=c+1
        a=a+1 

    with open(r"C:\Users\timchen\Desktop\notu class\專題\濁水溪shape file\GNSS\{}.json".format(gps_shp[i]), 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(geojson, ensure_ascii=False,indent=4) #將Python對象轉換為json字符串
        jsonf.write(jsonString)#另存一份json檔在資料夾裡 
        #print(jsonString)
print(geojson['features'][1])
      
