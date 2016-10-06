import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;


public class CreateClusters {

	
	public static void writeClusters(String inputfile,String outputfile) throws IOException{
		BufferedReader bR = new BufferedReader(new FileReader(inputfile));
		//BufferedWriter bW = new BufferedWriter(new FileWriter(outputfile));
		ArrayList<String> allLists = new ArrayList<String>();
		String nextLine;
		while((nextLine=bR.readLine())!=null){
			if(!nextLine.trim().isEmpty())
			allLists.add(nextLine);
		}
		for(int i=0; i< allLists.size();i++){
			for(int j=0; j<i;j++){
				System.out.println(allLists.get(i)+" "+allLists.get(j));
				//bW.write(allLists.get(i)+" "+allLists.get(j));
			}
		}
	}
	public static void main(String[] args) throws IOException{
		writeClusters("\\Users\\Digga_000\\Documents\\BitBucket\\Vocab\\good_words.txt","");
	}
	
}
