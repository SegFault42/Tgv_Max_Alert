#!/usr/bin/python

import urllib, json
import smtplib
import argparse
import datetime
import sys
import time

def parse_arguments():
    parser = argparse.ArgumentParser(description="TGV_Max_Alert")
    parser.add_argument('--date', type=str, required=True, help="date format : YYYY-MM-DD")
    parser.add_argument('--hour', type=str, required=True, help="hour format : 11:18. Monitor between 11h00 to 18h00")
    parser.add_argument('--origine', type=str, required=True, help="train station origine")
    parser.add_argument('--destination', type=str, required=True, help="train station destination")
    parser.add_argument('--alert', type=str, required=True, help="SMS/EMAIL/NO")
    parser.parse_args()
    args = parser.parse_args()
    return args

def is_args_valid(args):
    try:
        datetime.datetime.strptime(args.date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("\033[31mIncorrect data format, should be YYYY-MM-DD\033[0m")

    if (args.alert != "SMS" and args.alert != "EMAIL" and args.alert != "NO"):
        print ("\033[31mAlert bad formatted\033[0m")
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

def send_email(message):
    credential = json.load(open("./secret.json"))
    fromaddr = credential["EMAIL"]["my_email"]
    toaddrs = credential["EMAIL"]["toaddrs"]
    subject = "TGV MAX ALERT"

    msg = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (fromaddr, ", ".join(toaddrs), subject, message)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(credential["EMAIL"]["my_email"], credential["EMAIL"]["my_password"])
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()


def send_alert(data, args):
    message = "Train disponible " + data["fields"]["date"] + " !\n" +\
    "Aller : " + data["fields"]["origine"] +\
    "\nDepart a : " + data["fields"]["heure_depart"] +\
    "\nRetour : " + data["fields"]["destination"] +\
    "\nArrive a : " + data["fields"]["heure_arrivee"]
    print "\033[32m" + message + "\033[0m\n"
    if (args.alert == "SMS"):
        send_sms(message)
    elif (args.alert == "EMAIL"):
        send_email(message)

def search_train(data, my_hour, args):
    alert = False
    nb_train = len(data["records"])
    for i in range(0, nb_train):
        if (data["records"][i]["fields"]["od_happy_card"] == "OUI"):
            hour = data["records"][i]["fields"]["heure_depart"]
            hourIn = int(hour.split(':', 1)[0])
            if (int(my_hour[0]) <= hourIn and int(my_hour[1]) >= hourIn):
                send_alert(data["records"][i], args)
                alert = True
    if (alert == True):
        return True
    return False

def main():
    args = parse_arguments()
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

