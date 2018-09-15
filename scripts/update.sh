#!/bin/bash

### This script delete old database and update daily database from server with rsync

echo  "##################"
echo  "bandwidth info sync started at:"
date  +%c
echo  "##################"

DB_BACKUP_FILE="${TODAY}/bandwidth.tar.bz2"

cd "/home/shiva/w/bandwidth"
CWD="$(pwd)"
echo $CWD

# Archive old db 
tar -czvf "${CWD}${DB_BACKUP_FILE}" "bandwidth.db"

# delete old jalali database
rm bandwidth_jalali.db

# rsync new database
rsync -azP --stats --progress --times sls-streamer:/home/navaak/bandwidth.db ${CWD}

# run convert script to create new jalali db 
python3 convert_to_jalali.py


echo  "##################"
echo  "bandwidth info sync ended at:"
date  +%c
echo  "##################"