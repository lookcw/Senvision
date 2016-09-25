import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;

public class CompileWeekends {

	public static void compileWeekends(File[] files) {
		for (File file : files) {
			if (file.isDirectory()) {
				System.out.println("Directory: " + file.getName());
				File[] tweetsfiles = file.listFiles();
				for (File tweetFile : tweetsfiles) {
					String tweetDate = tweetFile.getName().substring(
							tweetFile.getName().indexOf("-"),
							tweetFile.getName().indexOf("Tweet"));
					SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
					Calendar current = Calendar.getInstance();
					try {
						current.setTime(sdf.parse(tweetDate));
					} catch (ParseException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
					if (current.get(Calendar.DAY_OF_WEEK) == 6
							|| current.get(Calendar.DAY_OF_WEEK) == 7) {
						String tweetFileName = file.getName() + "_"
								+ current.getTime() + "Tweets.txt";
						File tweetFile = new File(
								"C:\\Users\\Digga_000\\Documents\\BitBucket"
										+ tweetFileName);
						if (current.get(Calendar.DAY_OF_WEEK) == 6)
							current.add(current.DATE, -1);
						if (current.get(Calendar.DAY_OF_WEEK) == 7)
							current.add(current.DATE, -2);
						String fridayFileName = file.getName() + "_"
								+ current.getTime() + "Tweets.txt";

						File fridayTweetFile = new File(
								"C:\\Users\\Digga_000\\Documents\\BitBucket"
										+ fridayFileName);
						if (fridayTweetfile.exists()) {
								append(fridayTweetFile,tweetFile)
						}
					}
				}
			}
		}
	}
public static void append(File fileToAppendTo, File fileToAppend) throws IOException{
	BufferedWriter bW= new BufferedWriter( new FileWriter(fileToAppendTo,true));
	BufferedReader bR= new BufferedReader( new FileReader(fileToAppend));
	String nextLine;
	while((nextLine=bR.readLine())!=null){
		bW.write(nextLine);
	}
}

}
