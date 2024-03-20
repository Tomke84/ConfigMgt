# Python Project ConfigMgt

TO DO:

* fix linken in deploy bestand - creatie deployable versie van original json (naast processed versie)
* parameterlijst opslaan per project
* businessDomainProcessor afwerken + self-extract bij processTypes
* Sorteren op code activeren + verbeteren
* TST omgeving toevoegen
* extract valuelist toevoegen + self-extract bij businessDataTypes

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