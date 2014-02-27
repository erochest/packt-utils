#!/bin/bash

USAGE="$0 SUMMARY_LEVEL TABLE_CODE"

LLL="$1"
TT="$2"
STATES="01 02 04 05 06 08 09 11 11 12 13 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 72 44 45 46 47 48 49 50 51 53 54 55 56"
OUTPUT="all_${LLL}.${TT}.csv"

echo "Writing output to $OUTPUT."
touch $OUTPUT

# Handle the first state differently so we maintain the header line.
SS=01
curl http://censusdata.ire.org/${SS}/all_${LLL}_in_${SS}.${TT}.csv | gzcat > $OUTPUT

for SS in $STATES; do
	if [ $SS != "01" ]; then
		curl http://censusdata.ire.org/${SS}/all_${LLL}_in_${SS}.${TT}.csv | gzcat | tail -n +2 >> $OUTPUT
	fi
done
