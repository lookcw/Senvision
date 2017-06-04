cd ArticlesData
for d in */ ; do
cd $d
find . -type f -exec awk -v x=20 'NR==x{exit 1}' {} \; -exec rm -f {} \;
cd ..
done
cd ../Urls
for d in */ ; do
cd $d
find . -type f -exec awk -v x=20 'NR==x{exit 1}' {} \; -exec rm -f {} \;
cd ..
done
