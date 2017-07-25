import gspread
import csv
from oauth2client.service_account import ServiceAccountCredentials
 
 
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
 
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open_by_key("1ZRhTB_t_9cpjtdUhUpY5TkSPqHxrZ3fItpI2BIp8tvo")
print "why"
worksheet =sheet.get_worksheet(0)
print "whyyy"
print type(worksheet)
# Extract and print all of the values
#list_of_hashes = sheet.get_all_values()
#print(list_of_hashes)
f = open("../Results/Twitter_Future_Predictions.csv",'r')
results_reader=csv.reader(f,delimiter=',')
results_lines=list(results_reader)
print results_lines
for i in range(len(results_lines)):
	for j in range(len(results_lines[i])):
		print i," ",j
		if results_lines[i][j]=='+':
			worksheet.update_cell(i+1,j+1,"'+")
		else:
			worksheet.update_cell(i+1,j+1,results_lines[i][j])
#k=f.read()
#print k
#client.import_csv("1ZRhTB_t_9cpjtdUhUpY5TkSPqHxrZ3fItpI2BIp8tvo",k)
