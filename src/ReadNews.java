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

	public static String extractField(String field,String entry){
		int fieldIndex = entry.indexOf(field);
		int equalIndex = entry.indexOf("=",fieldIndex);
		int newLineIndex= entry.indexOf("\n",fieldIndex);
		
		return entry.substring(equalIndex+1,newLineIndex);
	}
	
	
public static String[] getUrlsFromRss(String Url) throws MalformedURLException, IOException, IllegalArgumentException, FeedException{
	SyndFeedInput input = new SyndFeedInput();
	XmlReader xReader = new XmlReader(new URL(Url));
	SyndFeed feed = input.build(xReader);
	String[] Urls= new String[feed.getEntries().size()];
	for(int i=0; i<feed.getEntries().size();i++){
		System.out.println(extractField("publishedDate",feed.getEntries().get(i).toString()));
		Urls[i]=extractField("link",feed.getEntries().get(i).toString());
	}
	return Urls;
	
}
	


public static String getBodyParagraph(String url) {
	Document doc;
	Elements paragraphs;
	try {
		doc = Jsoup.connect(url).get();
		//System.out.println(doc.select("p[class=article-published]").toString());
		paragraphs =doc.select("p");
	} catch (IOException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
		return null;
	}
	//System.out.println(doc.title());
	return doc.body().text();
//	return paragraphs.toString().replaceAll("<p>", " ");
}
	
public static String[] getBodiesFromRss(String rssLink) throws MalformedURLException, IllegalArgumentException, IOException, FeedException{
	String[] urls= getUrlsFromRss(rssLink);
	String[] articleTexts= new String[urls.length];
	for(int i=0;i<urls.length;i++){
		articleTexts[i]=getBodyParagraph(urls[i]);
	}
	return articleTexts;
	
}






public static void main(String[] args) throws MalformedURLException, IOException, IllegalArgumentException, FeedException{
	
	
String[] articleTexts= getBodiesFromRss("https://news.google.com/news?cf=all&hl=en&pz=1&ned=us&topic=b&output=rss");
System.out.println(articleTexts.length+"____________________________________");
for (String article:articleTexts){
	//System.out.println(article);
}
	/*
	Document doc = Jsoup.connect(link).get();
	Elements newsHeadlines = doc.select("p");
	System.out.println(doc.body().text());
	*/
	}
	
}
