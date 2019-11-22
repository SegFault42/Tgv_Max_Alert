# TGV MAX ALERT

### Usage :
```
$> git clone https://github.com/SegFault42/Tgv_Max_Alert
$> apt-get install python3-pip
$> pip3 install request
$> cd Tgv_Max_Alert
$> cp secret_template.json secret.json
```
Éditer le fichier secret Json avec vos informations.

Si vous souhaitez être notifie par email remplir les champs email avec un compte mail dans "my email".

Si vous souhaitez être notifie par SMS, remplir les champs SMS (fonctionne uniquement avec free mobile).  

[Configuration de la notification par SMS](https://www.freenews.fr/freenews-edition-nationale-299/free-mobile-170/nouvelle-option-notifications-par-sms-chez-free-mobile-14817)

```
-h, --help            		show this help message and exit
--date DATE			date format : YYYY-MM-DD
--hour HOUR			hour format : 11:18. Monitor between 11h00 to 18h00
--origine ORIGINE		train station origine
--destination DESTINATION	train station destination
--alert ALERT         		SMS/EMAIL/NO
--api                     getViaApi
```

Exemple pour un trajet entre Paris et Marseille :

```
python main.py --date="2018-03-26" --hour="6:20" --origine="PARIS (intramuros)" --destination="MARSEILLE ST CHARLES" --alert="EMAIL"
```

[Lien avec tous les noms des différentes gares](https://ressources.data.sncf.com/explore/dataset/tgvmax/?sort=date)

### Docker build
```
docker build -t tgvmax .
```

### Docker run
```
docker run -it \
  -v $(pwd):/folder \
  tgvmax "@"
```
