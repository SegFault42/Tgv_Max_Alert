#!/usr/bin/python

import urllib, json
import argparse
import datetime
import sys
#https://ressources.data.sncf.com/api/records/1.0/search/?dataset=tgvmax&sort=date&facet=date&facet=origine&facet=destination&refine.origine=PARIS+(intramuros)&refine.destination=BELFORT+MONTBELIARD+TGV&refine.date=2018-03-15

def parse_arguments():
    parser = argparse.ArgumentParser(description="TGV_Max_Alert")
    parser.add_argument('--date', type=str, required=True, help="date format : YYYY-MM-DD")
    parser.add_argument('--origine', type=str, required=True, help="train station origine")
    parser.add_argument('--destination', type=str, required=True, help="train station destination")
    parser.add_argument('--hour', type=str, required=True, help="hour format : 11:18. Monitor between 11h00 to 18h00")
    parser.parse_args()
    args = parser.parse_args()
    return args

def is_args_valid(args):
    try:
        datetime.datetime.strptime(args.date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("\033[31mIncorrect data format, should be YYYY-MM-DD\033[0m")
    hour = args.hour.split(':', 1)
    if (int(hour[0]) > 0 and int(hour[0]) < 24 and int(hour[1]) > 0 and int(hour[1]) < 24):
        return hour
    print ("\033[31mHour bad formatted\033[0m")
    sys.exit(-1)


def prepare_url(args):
    url = "https://ressources.data.sncf.com/api/records/1.0/search/?dataset=tgvmax&sort=date&facet=date&facet=origine&facet=destination"
    url += "&refine.origine=" + args.origine
    url += "&refine.destination=" + args.destination
    url += "&refine.date=" + args.date
    return url

def search_train(data, my_hour):
    #train_list =[]
    nb_train = int(data["nhits"])
    for i in range(0, nb_train):
        #print json.dumps(data["records"][i], indent=4)
        if (data["records"][i]["fields"]["od_happy_card"] == "OUI"):
            hour = data["records"][i]["fields"]["heure_depart"]
            hourIn = int(hour.split(':', 1)[0])
            if (int(my_hour[0]) <= hourIn and int(my_hour[1]) >= hourIn):
                #print json.dumps(data["records"][i]["fields"], indent=4)
                message = "Train available now !\n" + "Depart a : " + data["records"][i]["fields"]["heure_depart"] + " arrive a : " + data["records"][i]["fields"]["heure_arrivee"]
                print "\033[32m" + message + "\033[0m"
                message = ""
                return True
    return False

def main():
    args = parse_arguments()
    hour = is_args_valid(args)
    url = prepare_url(args)
    while (True):
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        #data = json.load(open("./ressources.data.sncf.com.json")) #debug for local test
        #print json.dumps(data["records"], indent=4)
        if search_train(data, hour) == True:
            return (1)
        sys.sleep(60)

if __name__ == '__main__':
    main()

