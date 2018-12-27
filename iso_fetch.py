import dryscrape
from bs4 import BeautifulSoup
from time import sleep
import csv
def parse(url):
    session = dryscrape.Session()
    session.visit(url)
    for i in range(3):
        sleep(5)
        try:
            response = session.body()
            soup = BeautifulSoup(response, "lxml")
            extract = (soup.find('div', class_='media-body'))
            extract_title = extract.text
        except Exception as e:
            print (e)
        return extract_title
def Read_ISO_NUM():
    #reader=['793:1973','430:1983','796:1973','431:1981','429:1983']#,'886:1973','428:1983', '795:1976', '808:1973', '886:1973', '2379:1972', '2142:1981',
            #'2107:1983','2092:1981','1338:1977','1337: 1980','1336:1980','1187: 1983']
    csv_file = open("ARAI.csv", 'r', encoding='utf-8', errors='ignore')
    reader = csv.reader(csv_file, delimiter=",", quotechar="'")
   # next(reader, None)
    with open('ARAI_output2.csv', 'w') as f:
      f = csv.write(f,delimiter='\t')
      #writer = csv.writer(f, delimiter='\t')
      #writer = csv.writer(f)
      for row in reader:
         row1=(','.join(row))
         url = "https://www.iso.org/search.html?q="+row1
         print("Processing: "+url)
         extracted_data=(parse(url))
         #print(extracted_data)
         sleep(5)
         f.write(row1)
         f.write("\t")
         #print(extracted_data)
         if row1 in extracted_data:
             f.write(extracted_data.replace(row1," ")[:99])
             #f.write(li_row.replace(li_out, " "))
             #print(extracted_data.replace(row1," ")[:99])
         else:
             #print(extracted_data[:99])
             f.write(extracted_data[:99])
         f.write("\n")
         #f.write(extracted_data)
         #f.write("\n")
    f.close()
    print("Done")

if __name__ == "__main__":
    Read_ISO_NUM()


