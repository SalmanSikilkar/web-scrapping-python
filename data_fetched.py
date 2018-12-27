import dryscrape
from bs4 import BeautifulSoup
import mysql.connector
import re
import sys
try:
   mydb = mysql.connector.connect(host='localhost',user='admin',passwd='admin@123',db='data_fetched')
   cursor = mydb.cursor()
   read = str(sys.argv[1])
   #read = str(input("enter the isbn number:"))
   #reader=["9350293471","9388369157","9385724060","9386797186","9386228343","9381626685","9385724061"]
   Titledb = Authordb = Pagesdb = Publisherdb = Languagedb = ISBN2db = Detailsdb = None
   #for read in reader:
   ISBN1db = read
   #print("Books isbn-10:",ISBN1db)
   url = "https://www.amazon.in/dp/" + read
   print(url)
   session = dryscrape.Session()
   session.visit(url)
   #sleep(2)
   response = session.body()
   soup = BeautifulSoup(response, "lxml")

   try:
           extract_title = soup.find('span', {'id': 'productTitle'})
           Title = extract_title.get_text()
           if Title:
               print("Book Title:", Title)
               Titledb = Title
           else:
               pass
   except:
           pass

   try:
           extract_author = soup.find('a', {'class': 'a-link-normal contributorNameID'})
           Author = extract_author.get_text()
           if Author:
               print("Book Author:", Author)
               Authordb = Author
           else:
               pass
   except:
       try:
           extract = soup.find_all('a', {'class': 'a-link-normal'})
           tags = []
           for tag in extract:
               if 'href' in tag.attrs and "author" in tag['href']:
                   (tags.append(tag))
           li = (re.sub("<.*?>", "", str(tags)))
           print("Book Author:",li.strip("[]"))
           Author =li.strip("[]")
           Authordb = Author
       except Exception as at:
           print(at)
           pass

   try:
           extract = soup.find('div', {'id': 'detail_bullets_id'})
           extract_detail = extract.find_all('li')[0:7]
           Pages = extract_detail[0].text
           Pages1 =extract_detail[1].text
           Pages2 = extract_detail[2].text
           Pages3 = extract_detail[3].text
           Pages4 = extract_detail[4].text
           Pages5 = extract_detail[5].text
           try:
               if Pages.split(":")[0] in ("Hardcover", "Paperback"):
                   print("Book1", Pages)
                   Pagesdb = Pages.split(":")[1]
               elif Pages1.split(":")[0] in ("Hardcover", "Paperback"):
                   print("Book2", Pages1)
                   Pagesdb = Pages1.split(":")[1]
               else:
                   Pagesdb = " "
           except:
               #print("NO Pages")
               pass

           try:
               if Pages1.split(":")[0] == "Publisher":
                   print("Book1", Pages1)
                   Publisherdb = Pages1.split(":")[1]
               elif Pages2.split(":")[0] == "Publisher":
                   print("Book2", Pages2)
                   Publisherdb = Pages2.split(":")[1]
               else:
                   Publisherdb = " "
           except:
               #print("NO Publisher")
               pass

           try:
               if Pages2.split(":")[0] == "Language":
                   print("Book1", Pages2)
                   Languagedb = Pages2.split(":")[1]
               elif Pages3.split(":")[0] == "Language":
                   print("Book2", Pages3)
                   Languagedb = Pages3.split(":")[1]
               else:
                   Languagedb = " "
           except:
               #print("NO Publisher")
               pass
           # try:
           #     ISBN1db = read
           # except:
           #     #print("NO ISBN-10")
           #     pass
           print("Books isbn-10:", ISBN1db)
           try:
               if Pages4.split(":")[0] == "ISBN-13":
                   print("Book1", Pages4)
                   ISBN2db = Pages4.split(":")[1]
               elif Pages5.split(":")[0] == "ISBN-13":
                   print("Book2", Pages5)
                   ISBN2db = Pages5.split(":")[1]
               else:
                   ISBN2db = " "
           except:
               pass
   except:
       pass
   try:
       extract = soup.select('div#bookDescription_feature_div noscript')[0].text
       #Det = extract.encode('utf-8')
       Det = extract.encode("ascii",'ignore')
       l = (re.sub("<.*?>", "",Det))
       li = re.sub(r"[^a-zA-Z]+", ' ',l)
       Detail = li.strip()
       #print(Detail)
       Detailsb = ((Detail[0:500] + '..') if len(Detail) > 500 else Detail)
       Detailsdb = Detailsb
       print("Abrstract",Detailsdb)
   except Exception as w:
       print(w)
       Detailsdb = " "
       pass
   try:
       li=[]
       extract_Subject = soup.find_all('a', {'class': 'a-link-normal a-color-tertiary'})
       for item in extract_Subject:
           li.append(item.text)
       Subject =  [line.replace(' ', '') for line in li]
       Subject_li= [rm.replace("\n","")for rm in Subject]
       Subjectb =",".join(Subject_li)
       Subjectdb = Subjectb
       print("Subjects:",Subjectdb)
   except Exception as my:
       print(my)
       Subjectdb= " "
       pass
   if Titledb == None:
           pass
   else:
     try:
       mydb = mysql.connector.connect(host='localhost', user='admin', passwd='admin@123', db='data_fetched')
       cursor = mydb.cursor()

       cursor.execute("INSERT  INTO amazon_data(title,author,pages,publisher,language,isbn_10,isbn_13,Details,Subjectdb)\
                          VALUES('%s', '%s','%s','%s','%s','%s','%s','%s',%s)" % 
                          (Titledb, Authordb, Pagesdb, Publisherdb, Languagedb, ISBN1db, ISBN2db,Detailsdb,Subjectdb,))
       print("Inserted into mysql")
       mydb.commit()
       cursor.close()
     except Exception as a:
         print(a)
         print("none")
except Exception as e:
       print(e)


