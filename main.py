#!/usr/bin/python

import urllib, json
import smtplib
import argparse
import datetime
import sys
import time
import requests
import datetime
import dateutil.parser
def parse_arguments():
    parser = argparse.ArgumentParser(description="TGV_Max_Alert")
    parser.add_argument('--date', type=str, required=True, help="date format : YYYY-MM-DD")
    parser.add_argument('--hour', type=str, required=True, help="hour format : 11:18. Monitor between 11h00 to 18h00")
    parser.add_argument('--origine', type=str, required=True, help="train station origine")
    parser.add_argument('--destination', type=str, required=True, help="train station destination")
    parser.add_argument('--alert', type=str, required=True, help="SMS/EMAIL/NO")
    parser.add_argument('--api', action="store_true", default=False)
    parser.parse_args()
    args = parser.parse_args()
    return args

def is_args_valid(args):
    try:
        datetime.datetime.strptime(args.date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("\033[31mIncorrect data format, should be YYYY-MM-DD\033[0m")

    if (args.alert != "SMS" and args.alert != "EMAIL" and args.alert != "NO"):
        print >> sys.stderr, "\033[31mAlert bad formatted.\033[0m"
        sys.exit(-1);

    hour = args.hour.split(':', 1)
    if (int(hour[0]) > 0 and int(hour[0]) < 24 and int(hour[1]) > 0 and int(hour[1]) < 60):
        return hour
    print ("\033[31mHour bad formatted\033[0m")
    sys.exit(-1)


def prepare_url(args):
    url = "https://ressources.data.sncf.com/api/records/1.0/search/?dataset=tgvmax&sort=date&facet=date&facet=origine&facet=destination"
    url += "&refine.origine=" + args.origine
    url += "&refine.destination=" + args.destination
    url += "&refine.date=" + args.date
    return url

def send_sms(message):
    credential = json.load(open("./secret.json"))
    print json.dumps(credential, indent=4)
    sms = "https://smsapi.free-mobile.fr/sendmsg?user="
    sms += credential["SMS"]["user"]
    sms += "&pass="
    sms += credential["SMS"]["password"]
    sms += "&msg="
    sms += message
    urllib.urlopen(sms)

def send_email(message, dest):
    try:
        jsonFile = open("./secret.json")
    except IOError:
        print >> sys.stderr, "\033[31mCould not open file!\033[0m"
        return (-1)

    credential = json.load(jsonFile)

    fromaddr = credential["EMAIL"]["my_email"]

    #toaddrs = credential["EMAIL"]["toaddrs"]
    subject = "TGV MAX ALERT"

    msg = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (fromaddr, ", ".join(dest), subject, message)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(credential["EMAIL"]["my_email"], credential["EMAIL"]["my_password"])
    server.sendmail(fromaddr, dest, msg)
    server.quit()
    jsonFile.close()


def send_alert(data, args, email):
    message = "Train disponible " + data["fields"]["date"] + " !\n" +\
    "Aller : " + data["fields"]["origine"] +\
    "\nDepart a : " + data["fields"]["heure_depart"] +\
    "\nRetour : " + data["fields"]["destination"] +\
    "\nArrive a : " + data["fields"]["heure_arrivee"]
    print "\033[32m" + message + "\033[0m\n"

    if (args.alert == "SMS"):
        send_sms(message)
    elif (args.alert == "EMAIL"):
        send_email(message, email)


def updateAlert(id):
    url = "http://tgv.baptisteheraud.com/api/alert/" + str(id)
    try:
        r = requests.post(
        url,
        params={},
        headers={'x-key': 'DemocracyIsFragil'},
        )
        json_response = r.json()
        if r.status_code != 200:
            print("\033[31m" + "Bad request API" +  "\033[0m")
            return (-1)
        return (json_response)
    except requests.exceptions.HTTPError as e:
        print ("ERROR")
        return (-1)

def getResearch():
    try:
        r = requests.get(
        'http://tgv.baptisteheraud.com/api/alert',
        params={},
        headers={'x-key': 'DemocracyIsFragil'},
        )
        json_response = r.json()
        if r.status_code != 200:
            print("\033[31m" + "Bad request API" +  "\033[0m")
            sys.exit(0)
        return (json_response)
    except requests.exceptions.HTTPError as e:
        print ("ERROR")
        sys.exit(0)


def prepare_alldatas(data):
    row = []
    for i in range(0, len(data)):
        format = '%Y-%m-%dT%H:%M:%S%z'
        d = dateutil.parser.parse(data[i]['goat'])   # python 2.7
        date = str(d.year) + "-" + str(d.month) + "-" + str(d.day)
        url = "https://ressources.data.sncf.com/api/records/1.0/search/?dataset=tgvmax&sort=date&facet=date&facet=origine&facet=destination"
        url += "&refine.origine=" + data[i]['departure']
        url += "&refine.destination=" + data[i]['arrival']
        url += "&refine.date=" + date
        value = [url, data[i]['user']['email'] , d, data[i]['id']]
        row.append(value)
    return (row)


def search_trainAPI(args):
    dataApi = getResearch()
    alldataApi = prepare_alldatas(dataApi)
    for k in range(0, len(alldataApi)):
        alert = False
        response = urllib.urlopen(alldataApi[k][0])
        datasncf = json.loads(response.read())
        nb_train = len(datasncf["records"])
        my_hour  = [alldataApi[k][2].hour, alldataApi[k][2].minute]

        dateAll =  str(alldataApi[k][2].day) + "/" + str(alldataApi[k][2].month) + "/" + str(alldataApi[k][2].year) + " " + str(my_hour[0]) + ":" + str(my_hour[1])
        print ("\n------")
        print ("Train pour %s le %s" % (alldataApi[k][1], dateAll ))
        print ("------\n")
        for i in range(0, nb_train):
            if (datasncf["records"][i]["fields"]["od_happy_card"] == "OUI"):
                hour = datasncf["records"][i]["fields"]["heure_depart"]
                hourIn = int(hour.split(':', 1)[0])
                minuteIn = int(hour.split(':')[1])
                if (int(my_hour[0]) <= hourIn):
                    if (int(my_hour[0]) == hourIn):
                        if int(my_hour[1]) <= minuteIn:
                            send_alert(datasncf["records"][i], args, alldataApi[k][1])
                            alert = True
                    else:
                        send_alert(datasncf["records"][i], args, alldataApi[k][1])
                        alert = True

        if alert == True:
            updateAlert(alldataApi[k][3])
                #print ("%s:%s" % (str(hourIn), str(minuteIn)))
    print ("-----------------------------------------------------")


def search_train(data, my_hour, args):
    alert = False
    nb_train = len(data["records"])
    for i in range(0, nb_train):
        if (data["records"][i]["fields"]["od_happy_card"] == "OUI"):

            hour = data["records"][i]["fields"]["heure_depart"]
            hourIn = int(hour.split(':', 1)[0])
            minuteIn = int(hour.split(':')[1])

            if (int(my_hour[0]) <= hourIn):
                if (int(my_hour[0]) == hourIn):
                    if int(my_hour[1]) <= minuteIn:
                        send_alert(data["records"][i], "ptilinux52@gmail.com")
                        alert = True
                else:
                    send_alert(data["records"][i], args , "ptilinux52@gmail.com")
                    alert = True
    if (alert == True):
        return True
    return False

def main():
    args = parse_arguments()


    if args.api:
        #dataApi = getResearch()
        #alldataApi = prepare_alldatas(dataApi)
        while (True):
            search_trainAPI(args)
            time.sleep(15)

    hour = is_args_valid(args)
    url = prepare_url(args)
    while (True):
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        if search_train(data, hour, args) == True:
            return (1)
        else:
            print "Aucun train disponible ..."
        time.sleep(60)

if __name__ == '__main__':
    main()
