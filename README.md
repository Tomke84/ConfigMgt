# Python Project ConfigMgt

TO DO:

* Moeten nog steeds valuelists uitgeprint worden op de console?
* fix linken in deploy bestand - creatie deployable versie van original json (naast processed versie)
* parameterlijst opslaan per project
* TST omgeving toevoegen
* Als REQUEST_ID en REQUEST_TIMESTAMP tussen de business data, dan melding om link met SERVICEREQUESTWEBCOMPONENT te maken!

commit "Improvements to sorting and deploy script"

* Clear cache requests toevoegen aan deploy script
* Implement sorting parentProcessTypes

commit "Improved sorting + general clean-up of code"

* code om json te sorteren verbeterd (nog niet helemaal op punt, maar we komen dichtbij)
* alle losse eindjes in de code opgeruimd zodat script kan gedeeld worden voor mijn verlof


commit "Adding self-extract business data from processes and tasks"

* businessDomainProcessor afwerken + self-extract bij processTypes


commit "bugfix self-extract business data from processes and tasks"

* PUT/POST on businessDataTypes doesn't exist --> only PATCH
* bugfix: save list_business_data in list_business_data.txt


commit "Adding self-extract business data from processes and tasks"

* businessDataTypes automatisch uit taken en processen halen


commit "Fix deploy_wave_configuration.py"

* updating links to filenames (forgotten in previous commit)
* added encoding utf-8 to files. With default encoder, it generated an error: 'charmap' codec can't decode byte 0x8f in position 10000. Ref: https://stackoverflow.com/questions/42019117/unicodedecodeerror-charmap-codec-cant-decode-byte-0x8f-in-position-xxx-char 


commit "Adding PRE and POST checks"

* Adding parameter for PRE and POST checks, so files and directories are named accordingly. This is to be able to compare a config in a certain enviromment before and after deploy.


commit "herstellen extract BuDaT + herbenoeming deploy script"

* herstellen extract BuDaT
* herbenoeming deploy script