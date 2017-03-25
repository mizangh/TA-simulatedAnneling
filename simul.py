# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 18:50:29 2017

@author: mizannn
"""
import math
import random
import googlemaps
import copy
import datetime

class City:
   def __init__(self, name, lat, lng, time, rating, jenisWisata):
      self.name = name
      self.lat = lat
      self.lng = lng
      self.time = time
      self.dttime = 0
      self.rating = rating
      self.jenisWisata = jenisWisata
      
   def __eq__(self, other): 
       return self.__dict__ == other.__dict__
   
   def getjenisWisata(self):
       return self.jenisWisata
       
   def getRating(self):
       return self.rating
   def getTime(self):
       return self.time
      
   def getName(self):
       return self.name
   def getLat(self):
      return self.lat
   
   def getLng(self):
      return self.lng
   
   def setDateTime(self,dttime):
       self.dttime = dttime
   
   def getDateTime(self):
       return self.dttime

   def __repr__(self):
      return str(self.getName()) + "(" + str(self.getDateTime()) + ")"


class TourManager:
   destinationCities = []
   
   def addCity(self, city):
      self.destinationCities.append(city)
   
   def getCity(self, index):
      return self.destinationCities[index]
   
   def numberOfCities(self):
      return len(self.destinationCities)

class Tour:
   def __init__(self, tourmanager, tour=None):
      self.tourmanager = tourmanager
      self.tour = []
      self.distance = 0
      if tour is not None:
         self.tour = copy.copy(tour)
      else:
         for i in range(0, self.tourmanager.numberOfCities()):
            self.tour.append(None)
   def __len__(self):
      return len(self.tour)
   
   def __getitem__(self, index):
      return self.tour[index]
   
   def __setitem__(self, key, value):
      self.tour[key] = value

   def __repr__(self):
      geneString = ""
      for i in range(0, self.tourSize()):
          if (i != (self.tourSize()-1)):
              geneString += str(self.getCity(i)) + " --> "    
          else:
              geneString += str(self.getCity(i))
      return geneString
 
   def getTour(self):
       return self.tour
       
   def hitungDistance(self,fromCity,targetCity): #menghitung distance dalam menit   
       time = []
       distance = 0
       my_distance = gmaps.distance_matrix(fromCity,targetCity)
       duration = str(my_distance['rows'][0]['elements'][0]['duration']['text'])
       for s in duration.split(): 
           if s.isdigit():
               time.append(int(s))
           if (len(time) > 1):
               distance = (time[0]*60) + time[1]
           else:
               distance = time[0]       
       return distance 

   def generateIndividual(self):
      for cityIndex in range(0, self.tourmanager.numberOfCities()):
         self.setCity(cityIndex, self.tourmanager.getCity(cityIndex))
      random.shuffle(self.tour)

   def getCity(self, tourPosition):
      return self.tour[tourPosition]
   
   def setCity(self, tourPosition, city):
      self.tour[tourPosition] = city
      self.distance = 0

   def getDistance(self,matrix):
      if self.distance == 0:
         popularTime = 0
         tourDistance = 0
         for cityIndex in range(0, self.tourSize()):
            fromCity = str(self.getCity(cityIndex).getName())
            destinationCity = None
            if cityIndex+1 < self.tourSize(): 
               popularTime = self.getCity(cityIndex+1).getTime() 
               destinationCity = str(self.getCity(cityIndex+1).getName())
            else:
               popularTime = self.getCity(0).getTime() 
               destinationCity = str(self.getCity(0).getName())
            tourDistance += (matrix[fromCity][destinationCity] + popularTime)
         self.distance = tourDistance
      return self.distance
      
   def getDateTimeTour(self,matrix):
       jam = 7
       menit = 0
       for cityIndex in range(0, self.tourSize()):
          City = self.getCity(cityIndex)
          fromCity = str(City.getName())
          destinationCity = None
          dttime = datetime.time(jam,menit)
          if cityIndex+1 < self.tourSize():
             self.getCity(cityIndex).setDateTime(dttime) 
             popularTime = self.getCity(cityIndex+1).getTime() 
             targetCity = self.getCity(cityIndex+1)
             destinationCity = str(targetCity.getName())
          else:
             self.getCity(cityIndex).setDateTime(dttime)
             popularTime = self.getCity(0).getTime() 
             targetCity = self.getCity(0)
             destinationCity = str(targetCity.getName())
          #diCek apakah waktu yang ada dalam time matrix
          try:
             waktu = matrix[fromCity][destinationCity]
          except KeyError:
             fromCity = str(City.getLat()) + ',' + str(City.getLng())
             destinationCity = str(targetCity.getLat()) + ',' + str(targetCity.getLng())
             waktu = self.hitungDistance(fromCity,destinationCity)            
          #waktu perjalanan ditambah waktu di tempat  
          waktu += popularTime
          menit += waktu
          if (menit > 59):
             jam += int(menit/60)
             menit = int(menit % 60)
             
   def tourSize(self):
      return len(self.tour)
   
   def matrixDistance(self):
        distance = 0
        mydict = {}
        for i in range(0, self.tourSize()):
            str_i = str(self.getCity(i).getName())
            mydict[str_i] = {}
            for j in range(0, self.tourSize()):
                fromCity = str(self.getCity(i).getLat()) + ',' + str(self.getCity(i).getLng())
                targetCity = str(self.getCity(j).getLat()) + ',' + str(self.getCity(j).getLng()) 
                distance = self.hitungDistance(fromCity,targetCity)
                str_j = str(self.getCity(j).getName())
                mydict[str_i][str_j] = distance
        return mydict 
        
   def addHotel(self,hotels):
       distance = 0
       temp = 0
       hotel = None
       htl = None
       for i in range(0, len(hotels)):
           fromCity = str(hotels[i].getLat()) + ',' + str(hotels[i].getLng())
           targetCity = str(self.getCity(0).getLat()) + ',' + str(self.getCity(0).getLng())
           distance = self.hitungDistance(fromCity,targetCity)
           if (i == 0) :
               temp = distance
               hotel = hotels[i]
           if (distance < temp):
               temp = distance
               hotel = hotels[i]
       htl = copy.copy(hotel)     
       self.tour.insert(0,htl)
       self.tour.append(hotel)
   
   def cloneWisata(self):#untuk copy data wisata selain wisata malam,kuliner dan penginapan
       clone = []
       lt = None 
       for i in range(0,len(self.tour)):
           lt = self.tour[i]
           if(lt.getjenisWisata() == "Wisata"):
               clone.append(lt)
       return clone                 
   
   def addKuliner(self,kuliners,matrix):
       distance = 0
       temp = 0
       kuliner = None
       kul = None
       listWisata = sorted(self.cloneWisata(), key=lambda city: city.rating)
       for tur in self.tour:
           if tur == listWisata[0]:
               self.tour.remove(tur)                          
               break
       self.getDateTimeTour(matrix)
       for tur in self.tour:
           if (tur.dttime.hour >= 11 and tur.dttime.hour <= 13):
               index = self.tour.index(tur)
               break
       for i in range(0, len(kuliners)):
           fromCity = str(kuliners[i].getLat()) + ',' + str(kuliners[i].getLng())
           targetCity = str(self.getCity(index).getLat()) + ',' + str(self.getCity(index).getLng())
           distance = self.hitungDistance(fromCity,targetCity)
           if (i == 0) :
               temp = distance
               kuliner = kuliners[i]
           if (distance < temp):
               temp = distance
               kuliner = kuliners[i]
       kul = copy.copy(kuliner)
       self.tour.insert(index+1,kul)
       self.getDateTimeTour(matrix)
       
           
def dummyMatrix():
    matrix = {'Gedung Sate': {'Gedung Sate': 1, 'TSM': 19, 'museum Geologi': 5, 'Braga Street': 18, 'Kebun Binatang': 9}, 'TSM': {'Gedung Sate': 22, 'TSM': 1, 'museum Geologi': 22, 'Braga Street': 26, 'Kebun Binatang': 28}, 'museum Geologi': {'Gedung Sate': 5, 'TSM': 18, 'museum Geologi': 1, 'Braga Street': 19, 'Kebun Binatang': 12}, 'Braga Street': {'Gedung Sate': 14, 'TSM': 16, 'museum Geologi': 13, 'Braga Street': 1, 'Kebun Binatang': 12}, 'Kebun Binatang': {'Gedung Sate': 12, 'TSM': 25, 'museum Geologi': 10, 'Braga Street': 20, 'Kebun Binatang': 1}}
    return matrix

def acceptanceProbability(energy,newEnergy,temperature):
    if(newEnergy<energy):
        return 1.0
    else:
        return math.exp((energy - newEnergy) / temperature)

if __name__ == '__main__':
   
   tourmanager = TourManager()
   gmaps = googlemaps.Client(key ='AIzaSyAKUbybyLOFoY_cDCKooF6xzk5a-TRknCI')
   # Create and add our cities
   city = City("Gedung Sate", -6.899925, 107.622966, 40, 4.4, 'Wisata')
   tourmanager.addCity(city)
   city2 = City("Braga Street", -6.917826, 107.609445, 120, 4, 'Wisata')
   tourmanager.addCity(city2)
   city3 = City("TSM", -6.925519, 107.636632, 120, 4.4, 'Wisata')
   tourmanager.addCity(city3)
   city4 = City("museum Geologi", -6.900506, 107.621469, 60, 4.5, 'Wisata')
   tourmanager.addCity(city4)
   city5 = City("Kebun Binatang", -6.889857, 107.606980, 80, 1.5, 'Wisata')
   tourmanager.addCity(city5)
   #Hotel
   hotel1 = City("Hotel Serela Cihampelas", -6.894651, 107.603948, 0, 0, 'Hotel')
   hotel2 = City("Hotel Novotel Bandung", -6.904876, 107.604154, 0, 0, 'Hotel')
   hotel3 = City("Ibis Bandung Trans Studio Hotel", -6.927539, 107.636373, 0, 0, 'Hotel')
   hotel4 = City("Hotel Santika Bandung", -6.907433, 107.611778, 0, 0, 'Hotel')
   #Kuliner
   kuliner1 = City("Restoran Kampung Daun", -6.816661, 107.589124, 60, 4.2, 'Kuliner')
   kuliner2 = City("Yoghurt Cisangkuy", -6.901792, 107.621454, 60, 4.0, 'Kuliner' )
   kuliner3 = City("Roemah Nenek", -6.904442, 107.623547, 60, 3.8, 'Kuliner')
   kuliner4 = City("Paskal Food Market", -6.914358, 107.592580, 60, 4.1, 'Kuliner')
   kuliner5 = City("Atmosphere Resort Cafe", -6.926668, 107.613403, 60, 4.1, 'Kuliner')
   #Wisata malam
   malam1 = City("Puncak Ciumbuleuit", -6.855040, 107.613628, 120, 4.1, 'Wisata Malam')
   malam2 = City("Caringin Tilu", -6.858503, 107.665246, 120, 4.3, 'Wisata Malam')
   malam3 = City("Dago Tea House", -6.869845, 107.617790, 120, 3.9, "Wisata Malam")
   malam4 = City("Puncak Bintang Bandung",-6.841478, 107.677284, 120, 4.4, "Wisata Malam")
   temp = 1000
   coolingrate = 0.003
   
   currentSolution = Tour(tourmanager)
   currentSolution.generateIndividual()
   timeMatrix = currentSolution.matrixDistance()
   #print (timeMatrix)
   currentSolution.getDateTimeTour(timeMatrix)
   print ("initial Solution Distance = " + str(currentSolution.getDistance(timeMatrix)))
   #print ("Tour ", currentSolution)    
   best = Tour(tourmanager,currentSolution.getTour())
   
   while(temp > 1):
       newSolution = Tour(tourmanager,currentSolution.getTour())
       tourPos1 =int(newSolution.tourSize() * random.random())
       tourPos2 =int(newSolution.tourSize() * random.random())
       citySwap1 = newSolution.getCity(tourPos1)
       citySwap2 = newSolution.getCity(tourPos2)
       newSolution.setCity(tourPos2,citySwap1)
       newSolution.setCity(tourPos1,citySwap2)
       currentEnergy = currentSolution.getDistance(timeMatrix)
       neighbourEnergy = newSolution.getDistance(timeMatrix)
       if (acceptanceProbability(currentEnergy, neighbourEnergy, temp) > random.random()):
           currentSolution = Tour(tourmanager,newSolution.getTour())
       if (currentSolution.getDistance(timeMatrix) < best.getDistance(timeMatrix)):
           best = Tour(tourmanager,currentSolution.getTour())
       
       temp *= (1-coolingrate)
   #print (timeMatrix) 
   best.getDateTimeTour(timeMatrix)
   print ("Final Solution Distance = "+ str(best.getDistance(timeMatrix)))
   #print "Tour ", best
   finalTour = Tour(tourmanager,best.getTour())
   hotels = [hotel1,hotel2,hotel3,hotel4]
   kuliners = [kuliner1,kuliner2,kuliner3,kuliner4,kuliner5] 
   finalTour.addHotel(hotels)
   finalTour.addKuliner(kuliners,timeMatrix)
   #finalTour.getDateTimeTour(timeMatrix)
   print ("Tour :" , finalTour)    