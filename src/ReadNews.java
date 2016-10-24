import com.sun.syndication.feed.synd.SyndFeed;
import com.sun.syndication.io.SyndFeedInput;
import com.sun.syndication.io.XmlReader;

public class ReadNews {
	SyndFeedInput input = new SyndFeedInput();
	SyndFeed feed = input.build(new XmlReader(new URL("https://news.google.com/news?cf=all&hl=en&pz=1&ned=us&output=rss"))));
}
