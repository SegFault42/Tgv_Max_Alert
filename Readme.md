### TGV MAX API

Liste des toutes les data : https://ressources.data.sncf.com/explore/dataset/tgvmax/table/?sort=date

Example pour un trajet de belfort (gare tgv) à Paris le 15/03/2018:

https://ressources.data.sncf.com/api/records/1.0/search/?dataset=tgvmax&sort=date&facet=date&facet=origine&facet=destination&refine.origine=PARIS+(intramuros)&refine.destination=BELFORT+MONTBELIARD+TGV&refine.date=2018-03-15

Nous avons un json avec toutes les infos.

Le champ "od_happy_card" sert à savoir si des billets sont disponible ou pas.


	$> python main.py -h
	Usage : python main.py -date -hour -origine -destination

	-d --date : 12/03/2018
	-h --hour : 11-18
	-o --origine : BELFORT MONTBELIARD TGV
	-D --destination : PARIS (intramuros)

le format de l'heure indique une tranche pendant laquel on souhaite vérifier la disponibilité des billets. Dans l'exemple au dessus sa signifie qu'on veut un billet entre 11h00 et 18h00

La liste pour le formattage du nom de la gare se trouve ici : https://ressources.data.sncf.com/explore/dataset/tgvmax/table/?sort=date&dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6InRndm1heCIsIm9wdGlvbnMiOnsic29ydCI6ImRhdGUifX0sImNoYXJ0cyI6W3sidHlwZSI6ImxpbmUiLCJmdW5jIjoiQ09VTlQiLCJzY2llbnRpZmljRGlzcGxheSI6dHJ1ZSwiY29sb3IiOiIjNjZjMmE1In1dLCJ4QXhpcyI6ImRhdGUiLCJtYXhwb2ludHMiOiIiLCJ0aW1lc2NhbGUiOiJ5ZWFyIiwic29ydCI6IiJ9XX0%3D

