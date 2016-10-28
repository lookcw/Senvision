cd ..
java -jar Jars/StockFetcher.jar
cd stock_data
python stocktable2.py
cd ..
#java -jar Jars/StockTweetPairer.jar
java -jar Jars/Vocab_Cluster_Generator.jar
#python testmodelclusters2.py
java -jar Jars/XValSetGenerator.jar
echo "completed"

