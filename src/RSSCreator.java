import java.io.IOException;
import java.net.MalformedURLException;

import com.sun.syndication.io.FeedException;

public class RSSCreator {
public static String[] searchterms= {"Intel", "Apple", "Merck", "Procter and Gamble", "Walmart", "Boeing","Morgan Chase","Google"};

public static void getRSS(String[] companies) throws MalformedURLException, IllegalArgumentException, IOException, FeedException, InterruptedException{
	for(String company:companies){
		Thread.sleep(1500);
		String[] allNews =ReadNews.getBodiesFromRss("www.faroo.com/api?q="+company+"&start=1&length=20&l=en&src=news&f=rss");
		for(String news: allNews){
			System.out.println(news);
		}
	}	
}

public static void main(String[] args) throws MalformedURLException, IllegalArgumentException, IOException, FeedException, InterruptedException{
	getRSS(searchterms);
}
}
