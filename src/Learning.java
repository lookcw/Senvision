import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;

import twitter4j.Query;
import twitter4j.QueryResult;
import twitter4j.Status;
import twitter4j.Twitter;
import twitter4j.TwitterException;
import twitter4j.TwitterFactory;
import twitter4j.conf.ConfigurationBuilder;

public class Learning {
	Twitter twitter;
	String[] searchterms = { "Intel", "Merck", "p&g", "Walmart", "Boeing", "Morgan Chase", "Google", "$INTC", "$AAPL",
			"$MRK ", "$PG ", "$WMT ", "$BA", "$JPM", "$GOOGL " };
	// ENGLISH COMPNAY NAMES MUST COME FIRST && ticker Names must be all
	// uppercase

	public Learning() throws TwitterException {
		ConfigurationBuilder cb = new ConfigurationBuilder();
		cb.setDebugEnabled(true).setOAuthConsumerKey("GkNo1eVzDrIvx4WX0UF2IQvUy")
				.setOAuthConsumerSecret("u44NuHRf7zWJS3oXNCMruJnDyUqugAKTYReSAV5cykHkQ3vxp5")
				.setOAuthAccessToken("763207677463920640-cTCEshVK13VFegFjrUry1p5tyUa98Ux")
				.setOAuthAccessTokenSecret("xx5fQbbIjv6zzGv7FrzUXdqxmpOe0tyO8s48zNApMG84y");
		TwitterFactory tf = new TwitterFactory(cb.build());
		twitter = tf.getInstance();
		twitter.verifyCredentials();
	}

	public String tickerToName(String tickerCompName) {
		String compname = tickerCompName;
		switch (tickerCompName) {
		case "p&g":
			compname = "Procter&Gamble";
			break;
		case "$INTC":
			compname = "Intel";
			break;
		case "$AAPL":
			compname = "Apple";
			break;
		case "$MRK ":
			compname = "Merck";
			break;
		case "$WMT ":
			compname = "Walmart";
			break;
		case "$PG ":
			compname = "Procter&Gamble";
			break;
		case "$BA":
			compname = "Boeing";
			break;
		case "$JPM":
			compname = "JPMorganChase";
			break;
		case "$GOOGL ":
			compname = "Google";
			break;
		case "$GOOGL":
			compname = "Google";
			break;
		case "Morgan Chase":
			compname = "JPMorganChase";
			break;
		}
		System.out.println(compname + " to " + tickerCompName);
		return compname;
	}

	/**
	 * Extracts a tweets of a query term from a certain day and puts it in
	 * /home/mankeyace/GitHub/stock/Tweets"+compname+"|"+dt+"Tweets.txt" where
	 * dt is the date
	 * 
	 * @param date
	 * @param queryterm
	 * @throws TwitterException
	 * @throws IOException
	 * @throws ParseException
	 */
	public int GetTweetsDay(String date, String queryterm) throws IOException, ParseException {
		String writeLine;
		ArrayList<String> noDuplicateTweets = new ArrayList<String>();
		Query query = new Query(queryterm + "+exclude:retweets").lang("en");
		boolean finished = false;
		int count = 0;
		String compname = this.tickerToName(queryterm);
		System.out.println("compname:" + compname);
		String dt = date; // Start date
		File companyFolder = new File("AllTweets/filteredTweets/" + compname);

		if (!companyFolder.exists()) {
			companyFolder.mkdir();
		}
		File filetomake;
		File finalFile = new File("AllTweets/filteredTweets/" + compname + "/" + compname + "_" + dt + "Tweets.txt");
		if (finalFile.exists()) {
			return 2;
		}
		File firstFile = new File("AllTweets/filteredTweets/" + compname + "/" + compname + "_" + dt + "Tweets+.txt");
		if (firstFile.exists() && queryterm.toUpperCase() != queryterm) { // if
																			// the
																			// intermediate
																			// file
																			// doesnt
																			// exist
																			// and
																			// its
																			// not
																			// on
																			// the
																			// ticker
																			// name
																			// quit
			return 2;

		}

		else if (!firstFile.exists() && queryterm.toUpperCase() == queryterm) {// if
																				// the
																				// intermediate
																				// file
																				// doesnt
																				// exist
																				// but
																				// its
																				// on
																				// the
																				// tickername
			filetomake = finalFile;

		} else if (firstFile.exists() && queryterm.toUpperCase() == queryterm) {// if
																				// intermediate
																				// file
																				// exists
			firstFile.renameTo(finalFile);// rename the intermediate to final
											// file
			filetomake = finalFile; // make the final file
		}

		else {
			filetomake = firstFile;
		}

		BufferedWriter bW;
		PrintWriter pW;
		if (queryterm.toUpperCase() == queryterm) {// companynames first
			System.out.println(queryterm + " Second part");
			bW = new BufferedWriter(new FileWriter(filetomake, true));
		} else
			bW = new BufferedWriter(new FileWriter(filetomake, false));
		pW = new PrintWriter(bW);
		while (!finished) {
			if (count == 179)
				finished = true;
			count++;

			SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
			Calendar c = Calendar.getInstance();
			c.setTime(sdf.parse(dt));
			c.add(Calendar.DATE, 1); // number of days to add
			String nextDay = sdf.format(c.getTime()); // dt is now the new date
			query.setSince(dt);
			query.setUntil(nextDay);
			QueryResult result = null;
			try {
				result = twitter.search(query);
				final List<Status> statuses = result.getTweets();
				long lowestStatusId = Long.MAX_VALUE;
				for (Status status : statuses) {
					// do your processing here and work out if you are
					// 'finished' etc...
					String stat = status.getText();
					String tweetNoURL = removeUrl(stat);
					if (!noDuplicateTweets.contains(tweetNoURL)) {
						writeLine = ReplaceTickers.replaceticks(tweetNoURL);
						String nextLine1 = writeLine.replaceAll("#", " ");
						// System.out.println(nextLine1);
						String nextLine2 = nextLine1.replaceAll("\\$", " ");
						String nextLine3 = nextLine2.replaceAll("@", " ");
						pW.println(nextLine3);
						noDuplicateTweets.add(tweetNoURL);
					}
					// Capture the lowest (earliest) Status id
					lowestStatusId = Math.min(status.getId(), lowestStatusId);
				}
				// Subtracting one here because 'max_id' is inclusive
				query.setMaxId(lowestStatusId - 1);
			} catch (TwitterException e) {
				filetomake.delete();
				// TODO Auto-generated catch block
				e.printStackTrace();
				return -1;
			}

		}
		pW.close();
		System.out.println(queryterm + " closed ");
		return 1;
	}

	/**
	 * 
	 * @param commentstr
	 * @return
	 */
	private static String removeUrl(String commentstr) {

		return commentstr.replaceAll("https?://\\S+\\s?", "");
	}

	/**
	 * Start may not be after enddate
	 * 
	 * @param startdate
	 * @param enddate
	 * @throws ParseException
	 * @throws IOException
	 * @throws InterruptedException
	 * @throws TwitterException
	 */
	public void runTweetCollection(String startdate, String enddate)
			throws ParseException, IOException, InterruptedException {
		String currentdate = startdate;
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
		Calendar current = Calendar.getInstance();
		current.setTime(sdf.parse(currentdate));
		Calendar end = Calendar.getInstance();
		end.setTime(sdf.parse(enddate));
		int success = 1;
		while (!current.getTime().equals(end.getTime())) {
			for (int i = 0; i < searchterms.length; i++) {
				System.out.println(searchterms[i] + " |" + sdf.format(current.getTime()) + "|");

				success = this.GetTweetsDay(sdf.format(current.getTime()).toString(), searchterms[i]);

				if (success == -1) {
					System.out.println("failed, waiting 16 minutes");
					Thread.sleep(1000 * 60 * 30);
					this.GetTweetsDay(sdf.format(current.getTime()), searchterms[i]);
				}
				if (success != 2) {
					Thread.sleep(1000 * 60 * 16);
				}

			}
			current.add(current.DATE, 1);
		}
	}

	public static void main(String[] args) throws TwitterException, IOException, ParseException, InterruptedException {
		System.out.println("please");
		Learning l = new Learning();
		Calendar c = Calendar.getInstance();
		Calendar d = Calendar.getInstance();
		c.add(Calendar.DATE, -1);
		// c.add(Calendar.MONTH,);
		d.add(Calendar.DATE, -8);
		// d.add(Calendar.MONTH,0);
		// System.out.println(removeUrl("asdf asdfa wefadf
		// ghttps://mail.google.com/mail/u/0/#inbox/1579b537485463c8
		// https://mail.google.com/mail/u/0/#inbox/1579b537485463c8)"));
		l.runTweetCollection(d.get(Calendar.YEAR) + "-" + d.get(Calendar.MONTH) + "-" + d.get(Calendar.DATE),
				c.get(Calendar.YEAR) + "-" + c.get(Calendar.MONTH) + "-" + c.get(Calendar.DATE));
	}

}