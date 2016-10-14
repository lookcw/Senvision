cd ..
java -jar StockDataRetriever.jar
java -jar Vocab_Cluster_Generator.jar
python testmodelclusters.py
java -jar XValSetGenerator.jar
echo "completed"

