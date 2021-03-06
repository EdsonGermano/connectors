import fme
import fmeobjects
import json
import urllib2
from urllib2 import URLError

# Construct URL for API call to Census
# example (commute time): http://api.census.gov/data/2013/acs1?get=NAME,B08303_001E,B08303_002E,B08303_003E,B08303_004E,B08303_005E,B08303_006E,B08303_007E,B08303_008E,B08303_009E,B08303_010E,B08303_011E,B08303_012E,B08303_013E&for=place:63000&in=state:53

class PythonCensusApiCityReader(object):
    def __init__(self):
        
        self.apikey = fme.macroValues['API_KEY']
        self.acsyear = fme.macroValues['ACS_YEAR']
        self.indicators = fme.macroValues['INDICATORS']
        self.url = fme.macroValues['URL']
        self.years = fme.macroValues['YEARS']
        self.cities = [fme.macroValues['CITY1'],fme.macroValues['CITY2'],fme.macroValues['CITY3'],fme.macroValues['CITY4'],fme.macroValues['CITY5'],fme.macroValues['CITY6'],fme.macroValues['CITY7'],fme.macroValues['CITY8']]

        self.log = fmeobjects.FMELogFile()

    def close(self):
		# loop through years
		lst_years = self.years.split(",")
		for year in lst_years:
			fips_city = ""
			fips_state = ""
			for city in self.cities:
				lst_location = city.split(",")
				fips_city = lst_location[0]
				fips_state = lst_location[1]
				feature_name = ""
				feature_value = ""
				indicator_url = ""
				indicator_url = self.url + year + '/acs' + self.acsyear + '?get=NAME,' + self.indicators + '&for=place:' + fips_city + '&in=state:' + fips_state + '&key=' + self.apikey
				self.log.logMessageString(indicator_url)
				req = urllib2.Request(indicator_url)
				opener = urllib2.build_opener()
				# make request to Census API
				try:
					f = opener.open(req)
					# load the JSON response
					response = json.loads(f.read())
					# if response consists of more than 1 record (first record consists of columns names), then return the row data to FME
					if len(response)>1:
						# loop through the rows of the response
						for n in range(len(response)):
							# create the FME feature object to store attributes to output
							feature = fmeobjects.FMEFeature()
							row = response[n]
							# loop through the columns of each row so we can output the values to FME - Note, all attributes need to be explicitly set in PythonCreator
							for i in range(len(row)):
								feature_name = "col" + str(i)
								feature_value = row[i]
								if feature_value == None:
									feature_value = ""
								feature.setAttribute(feature_name, feature_value)
							# output year
							feature.setAttribute("Year", year)
							# output each row's set of features to FME
							self.pyoutput(feature)
				except URLError, e:
					self.log.logMessageString(str(e), fmeobjects.FME_WARN)
					self.log.logMessageString("ACS Year " + str(self.acsyear) + " data may not be available yet for year "+str(year) + " and metro area "+str(city), fmeobjects.FME_WARN)
