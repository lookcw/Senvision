import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;

import com.opencsv.CSVReader;
import com.opencsv.CSVWriter;

public class PredictToday {

	
	
	
	public static void extractTodayDescriptor(String descriptorFile,String testingFile) throws IOException{
	CSVReader  descriptorReader = new CSVReader(new FileReader(descriptorFile));
	DateFormat f = new SimpleDateFormat("yyyy-MM-dd");
	/*
	String[] nextLine;
	cR.readNext();
	List<String[]> allDescriptors= new ArrayList<String[]>();
	while((nextLine=cR.readNext())!=null){
		allDescriptors.add(nextLine);
		
	}
	Collections.sort(allDescriptors, new Comparator<String[]>() {
        DateFormat f = new SimpleDateFormat("yyyy-MM-dd");
        @Override
        public int compare(String[] o1, String[] o2) {
            try {
            	Date date1= f.parse(o1[0]);
            	Date date2= f.parse(o2[0]);
                return date1.compareTo(date2);
            } catch (ParseException e) {
                throw new IllegalArgumentException(e);
            }
		}
    });
    */
	
	Calendar stockDate= Calendar.getInstance();
	Calendar tweetDate= Calendar.getInstance();
	if (stockDate.get(Calendar.DAY_OF_WEEK) == 6){ //if its a friday, predict on mondays stock data from fridays tweets
 		stockDate.add(Calendar.DATE, 3);
	}
	else 
		if(stockDate.get(Calendar.DAY_OF_WEEK) == 7) { //if its a Saturday predict on monday
			stockDate.add(Calendar.DATE, 2);
			
	}
		else
			stockDate.add(Calendar.DATE, 1); //if its Sun-thurs, predict on the next day.
	tweetDate=(Calendar) stockDate.clone();
	tweetDate.add(Calendar.DATE,-3);
	String[] nextLine;
	String[] descriptorPredict= new String[0];
	while((nextLine=descriptorReader.readNext())!=null){
		if(nextLine[0]==f.format(tweetDate)){
			descriptorPredict=nextLine;
			break;
		}
	}
	if(descriptorPredict.length==0){
		System.out.println("failed to find correct tweet descriptors");
		return;
	}
	descriptorPredict[0]=f.format(tweetDate);
	CSVWriter TestingWriter = new CSVWriter(new FileWriter(testingFile));
	TestingWriter.writeNext(descriptorPredict);
	TestingWriter.close();
	descriptorReader.close();
	}
	
	public static void makeAllTodayDescriptors(String descriptorFolder,String testingFolder){
		File[] desFiles = new File(descriptorFolder).listFiles();
		for(File desFile:desFiles){
			try {
				extractTodayDescriptor(desFile.getAbsolutePath(), testingFolder+"/"+desFile.getName().substring(0,desFile.getName().indexOf("_"))+"_TestingSet.csv");
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		
		}
	}
	public static void main(String[] args) throws IOException{
		makeAllTodayDescriptors("descriptors","TestingSets");
	}
	
}
