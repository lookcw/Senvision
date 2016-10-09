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

	public static void compileWeekends(File[] files,int lagtime) throws IOException {
		for (File file : files) {
			if (file.isDirectory()) {
				System.out.println("Company: " + file.getName());
				File[] tweetsfiles = file.listFiles();
				for (File tweetFile : tweetsfiles) {

					String tweetDate = tweetFile.getName().substring(tweetFile.getName().indexOf("_")+1,
							tweetFile.getName().indexOf("Tweet"));
					SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
					Calendar current = Calendar.getInstance();
					try {
						current.setTime(sdf.parse(tweetDate));
					} catch (ParseException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
					String tweetFileName = file.getName() + "_" + sdf.format(current.getTime()) + "Tweets.txt";
					File tweetTxtFile = new File(
							"../../AllTweets/filteredTweets/" + file.getName() + "/" + tweetFileName);
					
					
					if (current.get(Calendar.DAY_OF_WEEK) == 7-lagtime || current.get(Calendar.DAY_OF_WEEK) == Math.abs((8-lagtime)%7)) {
					
						//System.out.println(tweetTxtFile.getPath()+" "+ tweetTxtFile.exists()+" that the current day file exists");
						if (current.get(Calendar.DAY_OF_WEEK) == 7-lagtime){
							current.add(current.DATE, -1);
						}
						else  if(current.get(Calendar.DAY_OF_WEEK) ==  Math.abs((8-lagtime)%7));
							current.add(current.DATE, -2);
						
						String fridayFileName = file.getName() + "_" + sdf.format(current.getTime()) + "Tweets.txt";

						File fridayTweetFile = new File("../../AllTweets/filteredTweets/"+file.getName()+"/" + fridayFileName);
						System.out.println("appending "+tweetTxtFile.getName()+" to "+fridayTweetFile.getName());
						if (fridayTweetFile.exists()) {
						 	Runtime.getRuntime().exec(new String[]{"bash","-c","cat "+tweetTxtFile.getPath()+" >> "+fridayTweetFile.getPath()});
				
						}
						try {
							Thread.sleep(50);
						} catch (InterruptedException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
						System.out.println(tweetTxtFile.delete()+ " that "+ tweetTxtFile.getName()+"  has been deleted.");
						
					}
					
				}
			}
		}
	}

	public static void append(File fileToAppendTo, File fileToAppend) throws IOException {
		BufferedWriter bW = new BufferedWriter(new FileWriter(fileToAppendTo, true));
		BufferedReader bR = new BufferedReader(new FileReader(fileToAppend));
		String nextLine;
		int count=0;
		while ((nextLine = bR.readLine()) != null) {
			bW.write(nextLine);
			System.out.println(count);
			count++;
		}
		bW.close();
		bR.close();
	}
		public static void main(String[] args){
			File[] CompaniesArray = new File("../../AllTweets/filteredTweets/").listFiles();
			try {
				compileWeekends(CompaniesArray,3);
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	
}