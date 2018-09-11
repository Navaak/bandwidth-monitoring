#!/bin/bash

# This script delete old database and update daily database from server with rsync

echo  "##################"
echo  "bandwidth info sync started at:"
date  +%c
echo  "##################"


cd "/home/shiva/w/bandwidth"
CWD="$(pwd)"
echo $CWD

# delete old jalali database
rm bandwidth_jalali.db

# rsync new database
rsync -azP --stats --progress --times --delete sls-streamer:/home/navaak/bandwidth.db /home/shiva/w/bandwidth

# run convert script
python3 convert_to_jalali.py


echo  "##################"
echo  "bandwidth info sync ended at:"
date  +%c
echo  "##################"