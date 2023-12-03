# importing required modules
import PyPDF2
import pandas as pd 
import pdfplumber
import glob  
import os 

def get_region_data(path):
    files = glob.glob(path + 'Dailydata/*.pdf',  
                    recursive = True) 
    df_master = pd.DataFrame(columns = ['Category','NR','WR','SR','ER','NER','Total','Date'])

    skipped=[]

    for file in files:
        try:
            word = "A. Maximum Demand"
            lines = []

            file_name = os.path.basename(file)
            file_tuple = os.path.splitext(file_name)
            date_of_file = file_tuple[0].split("_")[0]
            print(date_of_file)


            with pdfplumber.open(file) as pdf:
                #for page in pdf.pages:
                first_page = pdf.pages[0]
                if 'National Load Despatch Centre' in first_page.extract_text():
                    page = pdf.pages[1]
                elif '(cid:3)' in first_page.extract_text():
                    page = pdf.pages[1]
                else:
                    page = pdf.pages[0]

                text = page.extract_text()
                print(text)
                for line in text.split('\n'):
                    lines.append(line)
            print(lines)
                        
            for i, line in enumerate(lines):
                if word==line or 'A. Power Supply Position at All India and Regional level'==line or 'A.PowerSupplyPositionatAllIndiaandRegionallevel' ==line or 'A.Power Supply Position at All India and Regional level' == line:
                    print("INSIDE")
                    new_lst = lines[i : i + 11]
            


            df_lst = []
            txt = new_lst[3].split(" ")
            col = new_lst[1].split(" ")
            col.insert(0,'Category')
            if ('Demand Met during Evening Peak hrs(MW) (at 19:00 hrs; from RLDCs)' not in new_lst[2] and 'Demand Met during Evening Peak hrs(MW) (at 20:00 hrs; from RLDCs)' not in new_lst[2] and 'Demand Met during Evening Peak hrs(MW) (at 1900 hrs; from RLDCs)' not in new_lst[2] and 'Demand Met during Evening Peak hrs(MW) (at 2000 hrs; from RLDCs)' not in new_lst[2] and 'DemandMetduringEveningPeakhrs(MW)(at20:00hrs;fromRLDCs)' not in new_lst[2] and 'DemandMetduringEveningPeakhrs(MW)(at2000hrs;fromRLDCs)' not in new_lst[2]):
            # if (new_lst[2] == 'Demand Met during Evening Peak hrs(MW)' or new_lst[2] == 'Demand Met during Evening Peak' or new_lst[2] == 'Demand Met during Evening Peak hrs(MW) (at 1900' or new_lst[2] == 'Demand Met during Evening Peak hrs(MW) (at'):
                print("HELOO")
                table_a = new_lst[3:]
                tmp = table_a[0].split(" ")
                tmp.insert(0,'Demand Met during Evening Peak hrs(MW)')
                df_lst.append(tmp)
                for i in table_a[2:]:
                    tmp = i.replace('*','')
                    tmp = tmp.split(')')[-1].split(" ")
                    str_tmp = str(i.split(')')[0]) + ')'
                    tmp.insert(0,str_tmp)
                    tmp = list(filter(None,tmp))
                    df_lst.append(tmp)
            else:
                table_a = new_lst[2:-2]
                print("TABLE")
                print(table_a)
                for i in table_a:
                    tmp = i.replace('*','')
                    tmp = tmp.split(')')[-1].split(" ")
                    print(tmp)
                    str_tmp = str(i.split(')')[0]) + ')'
                    tmp.insert(0,str_tmp)
                    print(tmp)
                    tmp = list(filter(None,tmp))
                    df_lst.append(tmp)

            # print(table_a)
            print(df_lst)

            # for i in list(range(5,11)):
            #     print("i ",i)
            #     new_lst[i].replace('*','')
            #     word = ['Peak Shortage (MW) ', 'Energy Met (MU) ', 'Hydro Gen(MU) ', 'Wind Gen(MU) ', 'Solar Gen (MU) ', 'Energy Shortage (MU) ']
            #     if word[i-5] in new_lst[i]:
            #         print("inside loop")
            #         tmp = new_lst[i].replace(word[i-5],'')
            #         tmp = tmp.split(" ")
            #         w = word[i-5].replace(' ','')
            #         tmp.insert(0,word[i-5])
            #         df_lst.append(tmp)

            # txt = new_lst[12].split(" ")
            # #print(txt)
            # txt.insert(0,'Maximum Demand Met during the day')
            # df_lst.append(txt)

            word = "E. Import/"
            new_lst = []

            for i, line in enumerate(lines):
                # print(line)
                if word.lower() in line.lower():
                    print('\n')
                    #print(word, 'string exists in file')
                    print('Line Number:', i)
                    print("\n**** Lines containing Keyword: \"" +word+ "\" ****\n") 
                    #print('Line:', line)
                    new_lst = lines[i : i + 5]
                    print("FOUND")
            print("IMPORT")
            # print(new_lst)

            for i in new_lst[2:]:
                tmp = i.split(" ")
                # print(tmp)
                tmp = list(filter(None,tmp))
                df_lst.append(tmp)
            print("in between")
            print(df_lst)

            word = 'F. Generation Outage(MW)'

            new_lst=[]

            for i, line in enumerate(lines):
                if word==line:
                    print('\n')
                    #print(word, 'string exists in file')
                    print('Line Number:', i)
                    print("\n**** Lines containing Keyword: \"" +word+ "\" ****\n") 
                    #print('Line:', line)
                    new_lst = lines[i : i + 4]
            print("SECTOR")
            for i in new_lst[2:]:
                tmp = i.replace(" Sector",'')
                print(tmp)
                tmp = tmp.split(" ")
                if (len(tmp)==8):
                    tmp.pop()
                print(tmp)
                df_lst.append(tmp)
            
            print("HERE")
            print(df_lst)

            word = 'G. Sourcewise generation (MU)'

            new_lst = []
            # print(lines)

            for i, line in enumerate(lines):
                if word==line or 'G. Sourcewise generation (Gross) (MU)'==line:
                    print('\n')
                    #print(word, 'string exists in file')
                    print('Line Number:', i)
                    print("\n**** Lines containing Keyword: \"" +word+ "\" ****\n") 
                    #print('Line:', line)
                    new_lst = lines[i : i + 6]

            for i in new_lst[2:]:
                flag=0
                if 'Thermal (Coal & Lignite) ' in i:
                    to_replace = 'Thermal (Coal & Lignite) '
                    flag = 1
                elif 'Gas, Naptha & Diesel' in i:
                    to_replace = 'Gas, Naptha & Diesel '
                    flag = 1
                elif 'RES (Wind, Solar, Biomass & Others)' in i:
                    to_replace = 'RES (Wind, Solar, Biomass & Others) '
                    flag = 1
                elif flag == 0:
                    tmp = i.split(" ")
                    if (len(tmp)==8):
                        tmp.pop()
                    df_lst.append(tmp)
                if flag == 1:
                    tmp = i.replace(to_replace,'')
                    w = to_replace.strip()
                    tmp = tmp.split(" ")
                    tmp.insert(0,w)
                    if (len(tmp)==8):
                        tmp.pop()
                    df_lst.append(tmp)

            print(df_lst)

            df = pd.DataFrame(columns=col)
            for i in range(len(df_lst)):
                print(i)
                print(df_lst[i])
                df.loc[i] = df_lst[i]

            df["Date"] = date_of_file
            df_master = pd.concat([df_master, df])
        except:
            skipped.append(file)

            pass

    df_master.to_csv("data/Region_data.csv")
    print(df_master)

    # Importing library
    import csv
    
    # opening the csv file in 'w+' mode
    file_csv = open(path + 'data/skipped.csv', 'w+', newline ='')
    
    # writing the data into the file
    with file_csv:    
        write = csv.writer(file_csv)
        write.writerows(skipped)

if __name__ == '__main__':
    get_region_data()