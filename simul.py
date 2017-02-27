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
   def __init__(self, name, lat, lng, time):
      self.name = name
      self.lat = lat
      self.lng = lng
      self.time = time
      self.dttime = 0
   
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
   
   '''    
   def distanceTo(self,city):
      time = []
      fromCity = str(self.getLat()) + ',' + str(self.getLng())
      targetCity = str(city.getLat()) + ',' + str(city.getLng())
      gmaps = googlemaps.Client(key ='AIzaSyBB04-FBelWsz5Cvjtse5ovPH79HUY-Bj0')
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
        
      
   def distance(self, city):
       
      xDistance = abs(self.getLat() - city.getLat())
      yDistance = abs(self.getLng() - city.getLng())
      distance = math.sqrt( (xDistance*xDistance) + (yDistance*yDistance) )
      return distance
   '''
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
      
   def generateIndividual(self):
      for cityIndex in range(0, self.tourmanager.numberOfCities()):
         self.setCity(cityIndex, self.tourmanager.getCity(cityIndex))
      random.shuffle(self.tour)
   def getCity(self, tourPosition):
      return self.tour[tourPosition]
   
   def setCity(self, tourPosition, city):
      self.tour[tourPosition] = city
      self.distance = 0
   '''def Distance(self):
      if (self.distance == 0):
          tour distance = 0
          for cityIndex in range(0, self.tourSize()):
              fromCity = self.'''
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
          fromCity = str(self.getCity(cityIndex).getName())
          destinationCity = None
          dttime = datetime.time(jam,menit)
          if cityIndex+1 < self.tourSize():
             self.getCity(cityIndex).setDateTime(dttime) 
             popularTime = self.getCity(cityIndex+1).getTime() 
             destinationCity = str(self.getCity(cityIndex+1).getName())
          else:
             self.getCity(cityIndex).setDateTime(dttime)
             popularTime = self.getCity(0).getTime() 
             destinationCity = str(self.getCity(0).getName())
          waktu = (matrix[fromCity][destinationCity] + popularTime)
          menit += waktu
          if (menit > 59):
             jam += int(menit/60)
             menit = int(menit % 60)
             
   def tourSize(self):
      return len(self.tour)
   
   def matrixDistance(self):
        distance = 0
        mydict = {}
        #filldict = {}
        for i in range(0, self.tourSize()):
            str_i = str(self.getCity(i).getName())
            mydict[str_i] = {}
            for j in range(0, self.tourSize()):
                time = []
                fromCity = str(self.getCity(i).getLat()) + ',' + str(self.getCity(i).getLng())
                targetCity = str(self.getCity(j).getLat()) + ',' + str(self.getCity(j).getLng()) 
                my_distance = gmaps.distance_matrix(fromCity,targetCity)
                duration = str(my_distance['rows'][0]['elements'][0]['duration']['text'])
                for s in duration.split(): 
                    if s.isdigit():
                        time.append(int(s))
                    if (len(time) > 1):
                        distance = (time[0]*60) + time[1]
                    else:
                        distance = time[0]
                #distance += 80
                str_j = str(self.getCity(j).getName())
                mydict[str_i][str_j] = distance
            
            #mydict[str_i] = filldict
            #filldict.clear()
        return mydict 
        
   def addHotel(self,hotels):
       distance = 0
       temp = 0
       hotel = None
       htl = None
       for i in range(0, len(hotels)):
           time = []
           fromCity = str(hotels[i].getLat()) + ',' + str(hotels[i].getLng())
           targetCity = str(self.getCity(0).getLat()) + ',' + str(self.getCity(0).getLng())
           my_distance = gmaps.distance_matrix(fromCity,targetCity)
           duration = str(my_distance['rows'][0]['elements'][0]['duration']['text'])
           for s in duration.split(): 
                    if s.isdigit():
                        time.append(int(s))
                    if (len(time) > 1):
                        distance = (time[0]*60) + time[1]
                    else:
                        distance = time[0]
           if (i == 0) :
               temp = distance
               hotel = hotels[i]
           if (distance < temp):
               temp = distance
               hotel = hotels[i]
       htl = copy.copy(hotel)     
       self.tour.insert(0,htl)
       self.tour.append(hotel)
       
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
   city = City("Gedung Sate", -6.899925, 107.622966, 40)
   tourmanager.addCity(city)
   city2 = City("Braga Street", -6.917826, 107.609445, 120)
   tourmanager.addCity(city2)
   city3 = City("TSM", -6.925519, 107.636632, 120)
   tourmanager.addCity(city3)
   city4 = City("museum Geologi", -6.900506, 107.621469, 60)
   tourmanager.addCity(city4)
   city5 = City("Kebun Binatang", -6.889857, 107.606980, 80)
   tourmanager.addCity(city5)
   hotel1 = City("Hotel Serela Cihampelas", -6.894651, 107.603948, 0)
   hotel2 = City("Hotel Novotel Bandung", -6.904876, 107.604154, 0)
   hotel3 = City("Ibis Bandung Trans Studio Hotel", -6.927539, 107.636373, 0)
   hotel4 = City("Hotel Santika Bandung", -6.907433, 107.611778, 0)

   temp = 1000
   coolingrate = 0.003
   
   currentSolution = Tour(tourmanager)
   currentSolution.generateIndividual()
   timeMatrix = currentSolution.matrixDistance()
   
   print "initial Solution Distance = " + str(currentSolution.getDistance(timeMatrix))
   print "Tour ", currentSolution    
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
   print timeMatrix 
   best.getDateTimeTour(timeMatrix)
   print "Final Solution Distance = "+ str(best.getDistance(timeMatrix))
   #print "Tour ", best
   finalTour = Tour(tourmanager,best.getTour())
   hotels = [hotel1,hotel2,hotel3,hotel4]
   finalTour.addHotel(hotels)
   timeMatrix = finalTour.matrixDistance()
   finalTour.getDateTimeTour(timeMatrix)
   print "Tour" , finalTour
    
      