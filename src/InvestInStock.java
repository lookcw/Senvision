import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import com.opencsv.CSVReader;

public class InvestInStock {
	
	
	public static Map<String,Double> getStockData(String stockFile) throws NumberFormatException, IOException{
		CSVReader cR = new CSVReader(new FileReader(stockFile));
		String[] readLine;
		Map<String, Double> dateAndAdj = new HashMap<String, Double>();
		while((readLine = cR.readNext()) != null){
			dateAndAdj.put(readLine[0],Double.parseDouble(readLine[9]));
			
		}
		return dateAndAdj;
	}
	
public static double Invest(String stockFile,String[] daysToInvest,double startingDollars) throws NumberFormatException, IOException{
	Double[] StockupDowns= new Double [daysToInvest.length];
	int i=0;
	int multiplier=1;
	Map<String,Double> stockChanges=getStockData(stockFile);
	for(String day: daysToInvest){
		multiplier*=1+stockChanges.get(day);
	}
	return startingDollars*multiplier;
}





}
