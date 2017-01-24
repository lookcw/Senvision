import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

import org.apache.commons.validator.routines.UrlValidator;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

public class EventRegistryUrlPulling {
	
	public static String getBodyParagraph(String url) {
		Document doc;
		Elements paragraphs;
		UrlValidator urlValidator = new UrlValidator();
		System.out.println("Url: "+url);
		if(urlValidator.isValid(url)){
		try {
			doc = Jsoup.connect(url).get();
			//System.out.println(doc.select("p[class=article-published]").toString());
			paragraphs =doc.select("p");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			//e.printStackTrace();
			System.out.println("Failed to retreive URL");
			return null;
		}
		//System.out.println(doc.title());
		return doc.body().text();
		}
		else
			return "";
//		return paragraphs.toString().replaceAll("<p>", " ");
	}
	public static void WriteArticles(String inputFolder,String outputFolder) throws IOException{
		File[] urlsFolder = new File(inputFolder).listFiles();
		String nextLine;
		for(File compFolder:urlsFolder){
			String company=compFolder.getName();
			if (!new File(outputFolder+"/"+company).exists()){
				new File(outputFolder+"/"+company).mkdir();
			}
			for(File urlList: new File(compFolder.getPath()).listFiles()){
				String date= urlList.getName().substring(urlList.getName().indexOf("_")+1,urlList.getName().indexOf("_Urls.txt"));
				if (!new File(outputFolder+"/"+company+"/"+company+"_"+date+"_Articles.txt").exists()){
				System.out.println(company+" "+date+"_____________________________________");
				BufferedReader urlReader= new BufferedReader(new FileReader(urlList));
				BufferedWriter articleWriter = new BufferedWriter(new FileWriter(outputFolder+"/"+company+"/"+company+"_"+date+"_Articles.txt"));
				while ((nextLine=urlReader.readLine())!=null){
						articleWriter.write(getBodyParagraph(nextLine)+"\n");
				}
				articleWriter.close();
				}
				else{
					System.out.println("skipping "+company+" "+date);
				}
			}
		}
		
		
	}
	public static void main(String[] args) throws IOException{
			WriteArticles("News/Urls","News/ArticlesData");
	}
}
