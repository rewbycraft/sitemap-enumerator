#!/bin/bash

rm -r dump
tar -xf "$1" dump/urls.txt
tar -xf "$1" dump/valid_sitemaps.txt

for i in "$1" dump/urls.txt dump/valid_sitemaps.txt ; do

	curl --upload-file "$i" -L https://transfer.archivete.am
	echo

done
