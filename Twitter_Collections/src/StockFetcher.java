import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.nio.channels.Channels;
import java.nio.channels.ReadableByteChannel;

import org.apache.commons.io.FileUtils;





import twitter4j.TwitterException;

public class StockFetcher {

	static String[] Tickername = new String[] { "INTC", "AAPL", "MRK", "PG",
			"WMT", "BA", "JPM", "GOOGL" };

	public static String tickerToName(String tickerCompName){
		String compname=tickerCompName;
		 switch (tickerCompName) {
        case "INTC":  compname = "Intel";
                 break;
        case "AAPL":  compname = "Apple";
                 break;
        case "MRK":  compname = "Merck";
                 break;
        case "WMT":  compname= "Walmart";
                 break;
        case "PG":  compname = "p&g";
                 break;
        case "BA":  compname = "Boeing";
                 break;
        case "JPM": compname="Morgan Chase";
       		 break;
        case "GOOGL ": compname="Google";
        break;
        case "GOOGL": compname="Google";
        break;
    }
		 return compname;
	}
	
	public static void fetchStock(int finalDateYear, int finalDateMonth,
			int finalDateday, int startDateYear, int startDateMonth,
			int startDateDay, String outputfolder) throws IOException {
		for (String stockSymbol : Tickername) {

			String url = "http://ichart.finance.yahoo.com/table.csv?" + "s="
					+ stockSymbol + "&d=" + finalDateMonth + "&e="
					+ finalDateday + "&f=" + finalDateYear + "&g=d&a="
					+ startDateMonth + "&b=" + startDateDay + "&c="
					+ startDateYear + "&ignore=.csv";
					
			//String url="http://ichart.finance.yahoo.com/table.csv?s=AAPL&d=9&e=12&f=2013&g=d&a=8&b=7&c=1984&ignore=.csv";
			URL website;
			website = new URL(url);
			File f = new File("../stock_data/auto_pulled_data/"
								+ tickerToName(stockSymbol) + ".csv");
			FileUtils.copyURLToFile(website, f);
			/*
		    BufferedReader in = new BufferedReader(
		            new InputStreamReader(website.openStream()));
		    String inputLine;
	        while ((inputLine = in.readLine()) != null)
	            System.out.println(inputLine);
	        in.close();
			try {
				website = new URL(url);
				ReadableByteChannel rbc = Channels.newChannel(website.openStream());
				FileOutputStream fos = new FileOutputStream(
						"../stock_data/auto_pulled_data/"
								+ tickerToName(stockSymbol) + ".csv");
				fos.getChannel().transferFrom(rbc, 0, Long.MAX_VALUE);
				
			} catch (MalformedURLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			*/
		}

	}
	public static void main(String[] args) throws IOException{ 
	fetchStock(2016,10,1,2016,8,7,"");
	}
}
