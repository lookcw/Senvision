import java.io.BufferedInputStream;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.util.Arrays;
import java.util.Random;
import java.util.Scanner;

public class CreateGoodBadClusters {

	public static int countLines(String filename) throws IOException {
		InputStream is = new BufferedInputStream(new FileInputStream(filename));
		try {
			byte[] c = new byte[1024];
			int count = 0;
			int readChars = 0;
			boolean empty = true;
			while ((readChars = is.read(c)) != -1) {
				empty = false;
				for (int i = 0; i < readChars; ++i) {
					if (c[i] == '\n') {
						++count;
					}
				}
			}
			return (count == 0 && !empty) ? 1 : count;
		} finally {
			is.close();
		}
	}

	public static void MakeClusters(String vocabFolder, String ClusterFolder,int numWordsInCluster, int numOfExtraDescriptors)
			throws IOException {
		File[] vocabfolder = new File(vocabFolder).listFiles();
		for (File vocabFile : vocabfolder) {
			Random generator = new Random(1);
			int numLines = countLines(vocabFile.getPath());
			int start;
			int end;
			int[] exists = new int[numWordsInCluster];
			String cluster;
			String content = new Scanner(vocabFile).useDelimiter("\\Z").next();
			String[] allWords = content.split("\\r?\\n");
			BufferedWriter bW = new BufferedWriter(new FileWriter(ClusterFolder + "/"
					+ vocabFile.getName().substring(0, vocabFile.getName().indexOf(".")) + "_clustered.txt"));
			//generating first descriptors based on order of words by 100 to include all of them
			for (int i = 0; i < numLines; i += numWordsInCluster) {
				cluster = "";
				start = i;
				if (i + numWordsInCluster > numLines) {
					start = numLines - numWordsInCluster-1;
					end = numLines - 1;
				} else
					end = i + numWordsInCluster;
				for (int j = start; j < end; j++) {
					cluster += allWords[j] + " ";
				}
				bW.write(cluster + "\r\n");
			}
			//makes randomly generated descriptors
			for (int i = 0; i < numOfExtraDescriptors; i++) {
				cluster = "";
				Arrays.fill(exists, -1);
				for (int k = 0; k < numWordsInCluster; k++) {

					int randNum = generator.nextInt(numLines);
					if (!Arrays.asList(exists).contains(randNum)) {
						exists[k] = randNum;
						cluster += allWords[randNum] + " ";
					} else
						k--;

				}
				bW.write(cluster + "\r\n");

			}

			bW.close();
		}
	}

	public static void main(String[] args) throws IOException {
		MakeClusters("Vocab", "Vocab_Clusters",100, 60);
	}

}
