
public class ReplaceTickers {
	public static String[] Tickernames={"INTC","AAPL","BA","MRK","PG","WMT","GOOGL"}; //order of these two arrays matter
	public static String[] CompNames={"Intel","Apple","Boeing","Merck","P&G","Walmart","Google"};
	
	public static String replaceticks(String input){
		String replacedTickerString=input;
		for(int i=0; i<Tickernames.length;i++){
			replacedTickerString=replacedTickerString.replaceAll(Tickernames[i],CompNames[i]);
		}
		return replacedTickerString;
	}
	
	
	}
