import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.net.URL;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import org.python.core.PyInteger;
import org.python.core.PyObject;
import org.python.core.PyException;
import org.python.util.PythonInterpreter;
 
import org.apache.commons.io.FileUtils;

import com.opencsv.CSVReader;
import com.opencsv.CSVWriter;

public class StockFetcher {

	static String[] tickername = { "INTC", "AAPL", "MRK ", "PG ", "WMT ", "BA", "JPM", "GOOGL " };

	public static String tickerToName(String tickerCompName) {
		String compname = tickerCompName;
		switch (tickerCompName) {
		case "INTC":
			compname = "Intel";
			break;
		case "AAPL":
			compname = "Apple";
			break;
		case "MRK ":
			compname = "Merck";
			break;
		case "WMT ":
			compname = "Walmart";
			break;
		case "PG ":
			compname = "Procter&Gamble";
			break;
		case "BA":
			compname = "Boeing";
			break;
		case "JPM":
			compname = "JPMorganChase";
			break;
		case "GOOGL ":
			compname = "Google";
			break;
		case "GOOGL":
			compname = "Google";
			break;
		}
		return compname;
	}

	public static void fetchStock(int finalDateYear, int finalDateMonth, int finalDateday, int startDateYear,
			int startDateMonth, int startDateDay, String outputfolder) throws IOException {
		for (String stockSymbol : tickername) {

			 SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
			 Calendar c = Calendar.getInstance();
			
			c.add(Calendar.DATE,-1);
			c.add(Calendar.MONTH,1);
			String url = "http://ichart.finance.yahoo.com/table.csv?" + "s=" + stockSymbol.trim() + "&d=" + c.get(Calendar.MONTH)
					+ "&e=" + c.get(Calendar.DATE) + "&f=" + c.get(Calendar.YEAR) + "&g=d&a=" + startDateMonth + "&b=" + startDateDay
					+ "&c=" + startDateYear + "&ignore=.csv";

			// String
			// url="http://ichart.finance.yahoo.com/table.csv?s=AAPL&d=9&e=12&f=2013&g=d&a=8&b=7&c=1984&ignore=.csv";
			URL website;
			website = new URL(url);
			File f = new File("stock_data/auto_pulled_data/" + tickerToName(stockSymbol) + ".csv");
			FileUtils.copyURLToFile(website, f);
			
		}

	}

	public static void addTwitterDatetoStockFolder(String inputfolder,String outputfolder,int numDaysToAdd){
		for(File Stockfile: new File(inputfolder).listFiles() ){
			try {
				addTwitterDatetoStockFile(Stockfile,outputfolder+"/"+Stockfile.getName().replaceAll(".csv", "")+".tsv",numDaysToAdd);
				System.out.println(Stockfile.getName());
			} catch (IOException | ParseException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			
		}
	}
	
	
	public static void addTwitterDatetoStockFile(File inputfile,String outputfile,int numDaysToAdd) throws IOException, ParseException{
		CSVReader cR = new CSVReader(new FileReader(inputfile),'\t');
		CSVWriter cW = new CSVWriter(new FileWriter(outputfile),'\t');
		String[] nextLine;
		nextLine = cR.readNext();
		//System.out.println(outputfile);
		System.out.println(nextLine);
		String[] writeLine=new String[nextLine.length];
		writeLine[0]=nextLine[0];
		writeLine[1]="Tweet Prediction Date";;
		for(int i=1;i<nextLine.length-1;i++){
			writeLine[i+1]=nextLine[i];
		}
		cW.writeNext(writeLine);
		while((nextLine=cR.readNext())!=null){
			writeLine = new String[nextLine.length];
			writeLine[0]=nextLine[0];
			SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
			 Calendar c = Calendar.getInstance();
			 c.setTime(sdf.parse(nextLine[0]));
			 c.add(Calendar.DATE,-1* numDaysToAdd);
			 writeLine[1]=sdf.format(c.getTime());
			 for(int i=1;i<nextLine.length-1;i++){
				 writeLine[i+1]=nextLine[i];
			 }
			 cW.writeNext(writeLine);
		}
		cW.close();
		
	}
	
	
	
	public static void main(String[] args) throws IOException {
	
		System.out.println("Program outputting most current Stock data to stock_data/tweet_date_data with 3 days of lag time");
	
		Calendar c = Calendar.getInstance();
		System.out.println(c.getTime());
		// c.add(Calendar.DATE, numDay);
		c.add(Calendar.DATE, -1);
		
		fetchStock(c.get(Calendar.YEAR), c.get(Calendar.MONTH), c.get(Calendar.DATE), 2016, 7, 5, "");
		 
        try
        {
            PythonInterpreter.initialize(System.getProperties(), System.getProperties(), new String[0]);
            PythonInterpreter interp = new PythonInterpreter();
            interp.execfile("stock_data/stocktable4java.py");
            interp.close();
        }
        catch(Exception e)
        {
            System.out.println(e.toString());
            e.printStackTrace();
        }
		
		addTwitterDatetoStockFolder("stock_data/cleaned_data", "stock_data/tweet_date_data", 3);
	}
}
