import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

import com.sun.syndication.feed.synd.SyndFeed;
import com.sun.syndication.io.FeedException;
import com.sun.syndication.io.SyndFeedInput;
import com.sun.syndication.io.XmlReader;

public class ReadNews {

public static void main(String[] args) throws MalformedURLException, IOException, IllegalArgumentException, FeedException{
	SyndFeedInput input = new SyndFeedInput();
	XmlReader xReader = new XmlReader(new URL("https://news.google.com/news?cf=all&hl=en&pz=1&ned=us&topic=tc&output=rss"));
	SyndFeed feed = input.build(xReader);
	System.out.println(feed.getEntries());
System.out.println(feed.getLinks().size());
	for (Object link: feed.getLinks()){
		System.out.println("asdfaaerea");
	}
	ArrayList<String> links= (ArrayList<String>) feed.getLinks();
			for(String link:links){
				System.out.println("adsfas"
						);

	Document doc = Jsoup.connect(link).get();
	Elements newsHeadlines = doc.select("p");
	System.out.println(doc.body().text());
	}
}}
