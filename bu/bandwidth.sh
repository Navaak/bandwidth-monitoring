#!/bin/bash
vnstat -u 

SQLITE="/usr/bin/sqlite3"
DB="/home/navaak/bandwidth.db"
IFACE="ens32"
YESTERDAY=`vnstat -d -i ${IFACE} | tail -4 | head -1 | tr -s ' ' | xargs`

# build sql date in yyyy-mm-dd format
DATE=`echo -n "${YESTERDAY}" | cut -d ' ' -f 1`
YEAR=`echo -n ${DATE} | cut -d '/' -f 3`
MONTH=`echo -n ${DATE} | cut -d '/' -f 1`
DAY=`echo -n ${DATE} | cut -d '/' -f 2`
SQLDATE="${YEAR}-${MONTH}-${DAY}"
RX=0
TX=0

# build RX field
# ignore KB
echo -n ${YESTERDAY} | cut -d '|' -f 1 | grep --quiet 'KB'
if [[ ${?} == 0 ]]; then
	RX=0
fi

# divide MB by 1000
echo -n ${YESTERDAY} | cut -d '|' -f 1 | grep --quiet 'MB'
if [[ ${?} == 0 ]]; then
	TMP=`echo -n ${YESTERDAY} | cut -d '|' -f 1 | cut -d ' ' -f 2`
	RX=`awk "BEGIN { printf \"%.2f\", ${TMP} / 1024 }"`
fi

# do nothing for GB
echo -n ${YESTERDAY} | cut -d '|' -f 1 | grep --quiet 'GB'
if [[ ${?} == 0 ]]; then
	RX=`echo -n ${YESTERDAY} | cut -d '|' -f 1 | cut -d ' ' -f 2`
fi

# multiply by 1000 for TB
echo -n ${YESTERDAY} | cut -d '|' -f 1 | grep --quiet 'TB'
if [[ ${?} == 0 ]]; then
	TMP=`echo -n ${YESTERDAY} | cut -d '|' -f 1 | cut -d ' ' -f 2`
	RX=`awk "BEGIN { printf \"%.2f\", ${TMP} * 1024 }"`
fi

# build TX field
# ignore KB
echo -n ${YESTERDAY} | cut -d '|' -f 2 | grep --quiet 'KB'
if [[ ${?} == 0 ]]; then
	TX=0
fi

# divide MB by 1000
echo -n ${YESTERDAY} | cut -d '|' -f 2 | grep --quiet 'MB'
if [[ ${?} == 0 ]]; then
	TMP=`echo -n ${YESTERDAY} | cut -d '|' -f 2 | cut -d ' ' -f 2`
	TX=`awk "BEGIN { printf \"%.2f\", ${TMP} / 1024 }"`
fi

# do nothing for GB
echo -n ${YESTERDAY} | cut -d '|' -f 2 | grep --quiet 'GB'
if [[ ${?} == 0 ]]; then
	TX=`echo -n ${YESTERDAY} | cut -d '|' -f 2 | cut -d ' ' -f 2`
fi

# multiply by 1000 for TB
echo -n ${YESTERDAY} | cut -d '|' -f 2 | grep --quiet 'TB'
if [[ ${?} == 0 ]]; then
	TMP=`echo -n ${YESTERDAY} | cut -d '|' -f 2 | cut -d ' ' -f 2`
	TX=`awk "BEGIN { printf \"%.2f\", ${TMP} * 1024 }"`
fi

# insert into database
${SQLITE} ${DB} "INSERT INTO daily (day_of_year, rx, tx) VALUES ('${SQLDATE}', ${RX}, ${TX})"

