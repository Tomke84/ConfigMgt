# Python Project ConfigMgt

commit "Fix deploy_wave_configuration.py"

* updating links to filenames (forgotten in previous commit)
* added encoding utf-8 to files. With default encoder, it generated an error: 'charmap' codec can't decode byte 0x8f in position 10000. Ref: https://stackoverflow.com/questions/42019117/unicodedecodeerror-charmap-codec-cant-decode-byte-0x8f-in-position-xxx-char 

commit "Adding PRE and POST checks"

* Adding parameter for PRE and POST checks, so files and directories are named accordingly. This is to be able to compare a config in a certain enviromment before and after deploy.

commit "herstellen extract BuDaT + herbenoeming deploy script"

* herstellen extract BuDaT
* herbenoeming deploy script