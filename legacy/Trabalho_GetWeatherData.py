# -*- coding: windows-1252 -*-
################################################################################
##
##	 Description:
##				  Script used to run the weather data from a weather api
##
##
##	 History:
##		 Name			   Date		Comment
##		-----------------  -----------  ------------------------------
##		 Soraia Tarrinha	 	20-12-2021	First Version
################################################################################
import requests
from geopy import distance
import numpy as np
import pandas as pd
from datetime import datetime
import json
from os import path
import io
from itertools import chain


ref_city = 'Peniche'
ListOfCities = ['Tomar','Coimbra','Braga', 'Castelo Branco', 'Beja', 'Sabugal', 'Lisboa', 'Viseu','Aljustrel', 'Leiria']
Key="97938e2e363fc7b425f46d9413606a03"
url_api = "http://api.openweathermap.org/data/2.5/weather"
filename='weatherdata.json'
rows_list = []
def prepare(city,city_name,distance):

    for x in distance:
        if(city_name==x['City']):
            distance_city=x['Distance']
    temp=(city['main']['temp']-273.15) 
    humidity=(city['main']['humidity'])
    pressure=(city['main']['pressure'])
    description=(city['weather'][0]['description'])
    wind_speed=(city['wind']['speed'])
    wind_deg=(city['wind']['deg'])
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%m-%Y %H:%M:%S")
    data = {'City':  city_name,
            'temp': temp,
         'humidity': humidity,
         'pressure': pressure,
         'description': description,
         'wind_speed':wind_speed,
         'wind_deg':wind_deg,        
        'Timestamp':timestampStr,
        'Distance':distance_city
    }
        
    rows_list.append(data)
    
    return rows_list
def getWeatherrefCity(cityref,Key,url_api):
    payload = { 'q':cityref , 'appid': Key}
    r = requests.get(url_api, params=payload)
    content = r.json()
    return content
def getWeatherCitydata(city,key,url_api):
        payload = { 'q':city , 'appid': key}
        r = requests.get(url_api, params=payload)
        content = r.json()
        return content

def getdistancerefCity(city):
    lat_city=(city['coord']['lat'])
    long_city=(city['coord']['lon'])
    return lat_city,long_city
def getdistanceCity(city,cityref_lat,cityref_long):
    lat_city=(city['coord']['lat'])
    long_city=(city['coord']['lon'])
    d = distance.distance((lat_city, long_city), (cityref_lat, cityref_long))
    dist=d.km
    return dist
distances=[]
content_refcity=getWeatherrefCity(ref_city,Key,url_api)
lat_refcity,long_refcity=getdistancerefCity(content_refcity)
def getCityDistances(ListOfCities,Key,ref_city):
    for city in ListOfCities:
        content=getWeatherCitydata(city,Key,url_api)
        distance_city=getdistanceCity(content,lat_refcity,long_refcity)
        data={
        'City':city,
        'Distance':distance_city }
        distances.append(data)
    DataRefCity={
        'City':ref_city,
        'Distance':0
    }
    distances.append(DataRefCity)
    return distances

def savetoJson(data,filename):
    if path.isfile(filename) is False:
        with open(filename, 'w') as db_file:
            db_file.write(json.dumps([]))
    with open(filename) as fp:
        listObj = json.load(fp)
    listObj.append(data)
    with open(filename, 'w') as json_file:
        json.dump(listObj, json_file, 
                        indent=4,  
                        separators=(',',': '), ensure_ascii=False)
 
def getWeatherData(ref_city,ListOfCities,key,distances,url_api,filename):
    cont_refcity=getWeatherrefCity(ref_city,key,url_api)
    rows_list=prepare(cont_refcity,ref_city,distances)
    for city in ListOfCities:
        content=getWeatherCitydata(city,key,url_api)
        rows_list=prepare(content,city,distances)
    savetoJson(rows_list,filename)
    return rows_list
distances_citys=getCityDistances(ListOfCities,Key,ref_city)
def load_data_to_dataframe(filename):
    with open('weatherdata.json') as json_file:
        data = json.load(json_file)
    #the data is a list of a list of dictonaries,so this method below was necessary to transform the data to a dataframe
    df =pd.DataFrame(list(chain.from_iterable(data)))
    return df





