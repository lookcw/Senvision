
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

import twitter4j.Query;
import twitter4j.QueryResult;
import twitter4j.Status;
import twitter4j.Twitter;
import twitter4j.TwitterException;
import twitter4j.TwitterFactory;
import twitter4j.conf.ConfigurationBuilder;





public class Learning {
	public static void setAuth() throws TwitterException, IOException{
		ConfigurationBuilder cb = new ConfigurationBuilder();
		cb.setDebugEnabled(true)
		  .setOAuthConsumerKey("GkNo1eVzDrIvx4WX0UF2IQvUy")
		  .setOAuthConsumerSecret("u44NuHRf7zWJS3oXNCMruJnDyUqugAKTYReSAV5cykHkQ3vxp5")
		  .setOAuthAccessToken("763207677463920640-cTCEshVK13VFegFjrUry1p5tyUa98Ux")
		  .setOAuthAccessTokenSecret("xx5fQbbIjv6zzGv7FrzUXdqxmpOe0tyO8s48zNApMG84y");
		//cb.setUser("coldplay");
		TwitterFactory tf = new TwitterFactory(cb.build());
		Twitter twitter = tf.getInstance();
		twitter.verifyCredentials();
	       /*
	        Query query = new Query("Boeing");
	        query.setCount(100);
		    QueryResult result = twitter.search(query);
		    for (Status status : result.getTweets()) {
		        System.out.println("@" + status.getUser().getScreenName() + ":" + status.getText());
		    }
		    */
		String searchterm="Walmart";
		Query query = new Query(searchterm+"+exclude:retweets");
		  boolean finished = false;
		  int count=0;
		  BufferedWriter bW = new BufferedWriter(new FileWriter("../../Stock_Market_Prediction/Tweets/"+searchterm+"Tweets.txt",true));
		  while (!finished) {
			  if (count==100)
				  finished=true;
			  count++;
			  System.out.println(count);
			  query.setSince("2016-08-08"); 
		      query.setUntil("2016-08-09");
		      final QueryResult result = twitter.search(query);    
		      
		      final List<Status> statuses = result.getTweets();
		      long lowestStatusId = Long.MAX_VALUE;
		      for (Status status : statuses) {
		          // do your processing here and work out if you are 'finished' etc... 
		    	  bW.write(status.getText() + "\r\n");
		    //	  System.out.println(status.getText());
		    	// System.out.println( status.getCreatedAt().toGMTString());
		          // Capture the lowest (earliest) Status id
		          lowestStatusId = Math.min(status.getId(), lowestStatusId);
		      }
		      // Subtracting one here because 'max_id' is inclusive
		      query.setMaxId(lowestStatusId - 1);
		  }
		  bW.close();
	}
	
	public static void main(String[] args) throws TwitterException, IOException{
setAuth();
	
	    }
    
}
