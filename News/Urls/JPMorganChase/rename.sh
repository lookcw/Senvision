for f in *.txt; do
newname="$(echo "$f" | cut -c15- )"
newname=JPMorganChase"$newname"
echo $newname 
mv $f $newname
#mv -- "$f" "${f%.txt}"
#echo "$newname"
done
