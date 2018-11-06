import requests as req
import untangle
import json
from datetime import time, date, datetime

ACCESSTOKEN = "919c2d52-2249-4e32-bb3a-a61be9b545f4"

class nat_rail_api:
    def __init__(self):
        pass
    
    def get_live_times(self, station):
        URL = "https://lite.realtime.nationalrail.co.uk/OpenLDBWS/ldb6.asmx"
        reqStr = '<?xml version="1.0"?><SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://thalesgroup.com/RTTI/2014-02-20/ldb/" xmlns:ns2="http://thalesgroup.com/RTTI/2010-11-01/ldb/commontypes"><SOAP-ENV:Header><ns2:AccessToken><ns2:TokenValue>' + ACCESSTOKEN + '</ns2:TokenValue></ns2:AccessToken></SOAP-ENV:Header><SOAP-ENV:Body><ns1:GetDepartureBoardRequest><ns1:numRows>10</ns1:numRows><ns1:crs>' + station + '</ns1:crs></ns1:GetDepartureBoardRequest></SOAP-ENV:Body></SOAP-ENV:Envelope>'
        headers = {'Content-Type': 'text/xml'}
        r = req.post(URL, data=reqStr, headers = headers)
        print("StatusCode = " + str(r.status_code))
        print('\n')
        parsed_xml = untangle.parse(r.text)
        for i in parsed_xml.soap_Envelope.soap_Body.GetDepartureBoardResponse.GetStationBoardResult.lt2_trainServices:
            for j in i.lt2_service:
                print(j.lt2_origin.lt2_location.lt2_locationName.cdata + " to " + j.lt2_destination.lt2_location.lt2_locationName.cdata)
                print('\n')
    def get_historical_data(self, fromStation, toStation, fromTime, toTime, fromDate, toDate, days):

        URL = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Authorization': 'Basic Z2VvcmdlLm1hcmtoYW1AdWVhLmFjLnVrOlcjbiE1bU03MSY2N1hQRzNUNzI1'
        }
        data = {
            "from_loc": fromStation, 
	        "to_loc": toStation, 
	        "from_time": fromTime, 
	        "to_time": toTime, 
	        "from_date": fromDate, # Looks like 2018-11-05
	        "to_date": toDate,
	        "days": days #e.g WEEKDAY, WEEKEND
        }

        r = req.post(URL, data=json.dumps(data), headers=headers)
        res = json.loads(r.text)
        for service in res['Services']:
            rids = service['serviceAttributesMetrics']['rids']
            for rid in rids:
                # request individual train journey data
                URL = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"
                data = {"rid": rid}
                headers = {
                    'Content-Type': "application/json",
                    'cache-control': "no-cache",
                    'Authorization': 'Basic Z2VvcmdlLm1hcmtoYW1AdWVhLmFjLnVrOlcjbiE1bU03MSY2N1hQRzNUNzI1'
                }
                r = req.post(URL, data=json.dumps(data), headers=headers)
                res = json.loads(r.text)
                stations = res['serviceAttributesDetails']['locations']
                date_of_service = self.str_to_date(res['serviceAttributesDetails']['date_of_service'])
                print "\n"
                print "rid: ", rid
                for station in stations:
                    print station['location']
                    print "\tScheduled arrival time", station['gbtt_pta']
                    print "\tScheduled departure time", station['gbtt_ptd']
                    print "\tActual arrival time", station['actual_ta']
                    print "\tActual departure time", station['actual_td']
                    if len(station['gbtt_pta']) > 0 and station['actual_ta']:
                        print "\tDifference in arrival time", ( self.str_to_datetime(station['actual_ta'], date_of_service) - self.str_to_datetime(station['gbtt_pta'], date_of_service))
                    if len(station['gbtt_ptd']) > 0 and station['actual_td']:
                        print "\tDifference in departure time", ( self.str_to_datetime(station['actual_td'], date_of_service) - self.str_to_datetime(station['gbtt_ptd'], date_of_service) )
                    print "\n"
            
    def str_to_datetime(self, time_str, date_of_service):
        hrs = int(time_str[:2])
        mins = int(time_str[2:])
        return datetime.combine( date_of_service,  time(hrs, mins))

    def str_to_date(self, date_of_service):
        return datetime.strptime(date_of_service, '%Y-%m-%d')

def main():
    api = nat_rail_api()
    api.get_historical_data("MNG", "NRW", "0600", "0700", "2016-10-01", "2018-10-01", "WEEKDAY")

if __name__ == '__main__':
    main()