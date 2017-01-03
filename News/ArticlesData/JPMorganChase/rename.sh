for f in *.txt; do
newname="$(echo "$f" | cut -c3-)"
echo $newname
newname=Proctor\&Gamble"$f" 
#mv $f $newname
#mv -- "$f" "${f%.txt)}.txt"
echo "$newname"
done
