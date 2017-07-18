import gspread
from oauth2client.service_account import ServiceAccountCredentials
 
 
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
 
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("DIDMBT")
 
# Extract and print all of the values
#list_of_hashes = sheet.get_all_values()
#print(list_of_hashes)
f = open("../Results/News_Future_Predictions.csv",'r')
k=f.read()
print k

client.import_csv("1ZRhTB_t_9cpjtdUhUpY5TkSPqHxrZ3fItpI2BIp8tvo",k)