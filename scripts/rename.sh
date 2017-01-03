for f in *.txt; do
#newname="$(echo "$f" | cut -c26- )"
#newname=Procter\&Gamble"$newname"
#echo $newname 
#mv $f $newname
mv -- "$f" "${f%.txt}"
#echo "$newname"
done
