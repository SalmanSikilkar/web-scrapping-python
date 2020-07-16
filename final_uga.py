import dryscrape
from bs4 import BeautifulSoup
from time import sleep
import csv
with open('final_output1.csv', 'w') as f:
    writer = csv.writer(f)
    for a in range(0, 1020):
        try:
            url = "https://www.ugc.ac.in/uni_contactinfo.aspx?id=" + str(a)  # "1030"
            print(url)
            session = dryscrape.Session()
            session.visit(url)
            sleep(3)
            response = session.body()
            soup = BeautifulSoup(response, "lxml")
            rows = soup.findAll("tr")
            flat_list = []
            for row in rows:
                row1 = row.get_text()
                flat_list.append(row.get_text())
            # print(flat_list[3])
            try:
                data = soup.get_text()
                # print(data)
                # print(soup)
                extract_title = soup.find('font', {'face': 'arial'})
                Title = extract_title.get_text()
                #print(Title)
                f.write("\n")
                f.write(Title)
                f.write("\t")
                vcname = flat_list[2]
                vcname1 = vcname.split("VC Name:", 1)[1]
                vcname2 = vcname1.split("Phone No", 1)[0]
                vcname3=vcname2.strip()
                #print(vcname2)
                f.write(vcname3)
                f.write("\t")
                #f.write("\t")
                vcemail = vcname.split("E-mail:", 1)[1]
                #print(vcemail)
                vcemail1 =vcemail.strip()
                f.write(vcemail1)
                f.write("\t")
                #f.write("\t")
                rgname = flat_list[3]
                # print(rgname)
                rgname1 = rgname.split("Reg. Name:", 1)[1]
                rgname2 = rgname1.split("Phone No", 1)[0]
                #print(rgname2)
                #f.write("\t")
                rgname3 =rgname2.strip()
                f.write(rgname3)
                f.write("\t")
                rgemail = rgname.split("E-mail:", 1)[1]
                #print(rgemail)
                rgemail1 =rgemail.strip()
                f.write(rgemail1)
                #f.write("\t")
                #print("end")
            except:
                print("Notfound")
        except:
            print("concention refused")
        #f.write("\n")
    f.close()

