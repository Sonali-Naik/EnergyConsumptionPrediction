import pandas as pd 
import pdfplumber
import glob  
import os

def get_demand_data(path):
    word1 = "C. Power Supply Position in States"
    word2 = "D. Transnational Exchanges (MU) - Import(+ve)/Export(-ve)"    
    files = glob.glob(path + 'Dailydata/*.pdf',  
                    recursive = True) 
    df_master = pd.DataFrame(columns = ['States', 'Max. Demand Met during the day (MW)', 'Shortage during maximum Demand (MW)', 'Energy Met (MU)',
                                        'Drawal Schedule (MU)', 'OD(+)/UD(-) (MU)', 'Max OD (MW)', 'Energy Shortage (MU)'])
    # files = ['C:/Users/SONALI/OneDrive/Documents/ISB/Term5/FP2/Dailydata/02.06.18_NLDC_PSP.pdf']

    skipped=[]

    for file in files:
        try:
            lines = []

            file_name = os.path.basename(file)
            file_tuple = os.path.splitext(file_name)
            date_of_file = file_tuple[0].split("_")[0]
            print(date_of_file)

            with pdfplumber.open(file) as pdf:
                first_page = pdf.pages[0]
                if 'National Load Despatch Centre' in first_page.extract_text():
                    page = pdf.pages[1]
                elif '(cid:3)' in first_page.extract_text():
                    page = pdf.pages[1]
                else:
                    page = pdf.pages[0]

                text = page.extract_text()
                # print(text)
                text = text.replace('Railways_NR ISTS', 'Railways_north')
                text = text.replace('Railways_SR ISTS', 'Railways_south')
                text = text.replace('Railways_ER ISTS', 'Railways_east')
                text = text.replace('Railways_WR ISTS', 'Railways_west')
                text = text.replace('Railways_NER ISTS', 'Railways_northeast')
                to_replace = ['NR','WR','SR','NER','ER']
                for i in to_replace:
                    text = text.replace(i,'')
                # print(text)
                text = text.lower()
                state = ['Andhra Pradesh','Tamil Nadu','Arunachal Pradesh','West Bengal','Essar steel','j&k(ut) & ladakh(ut)', 'j&k(ut) and ladakh(ut)']
                for i in state:
                    print(i.lower())
                    if i.lower() in text:
                        print("yes")
                        rep = i.lower().replace(' ','')
                        print(rep)
                        text = text.replace(i.lower(),rep)
                # print(text)
                        
                for line in text.split('\n'):
                    lines.append(line)
                lines = list(filter(None,lines))


            print(lines)

                        
            # for i, line in enumerate(lines):
            #     if word1.lower()==line:
            #         start = i
            #         print("START",i)
            #     if word2.lower()==line:
            #         end = i
            #         break
            # lines = lines[start:end]

            # print(new_lst)

            for i in range(len(lines)):
                if 'punjab' in lines[i].lower():
                    index = i
                if word2.lower()==lines[i]:
                    endi = i
                    break

            demand_lst = lines[index:endi]
            print(demand_lst)
            df_lst = []
            for i in demand_lst:
                tmp = i.split(" ")
                tmp = list(filter(None,tmp))
                df_lst.append(tmp)

            df = pd.DataFrame(columns = ['States', 'Max. Demand Met during the day (MW)', 'Shortage during maximum Demand (MW)', 'Energy Met (MU)',
                                        'Drawal Schedule (MU)', 'OD(+)/UD(-) (MU)', 'Max OD (MW)', 'Energy Shortage (MU)'])

            for i in range(len(df_lst)):
                print(i)
                print(df_lst[i])
                df.loc[i] = df_lst[i]

            df["Date"] = date_of_file

            df_master = pd.concat([df_master, df])
        
        except :
            skipped.append(file)
            print("SKIPPED")
            pass

    df_master.to_csv(path + "data/Demand_data.csv")
    print(df_master)

    # Importing library
    import csv
    
    # opening the csv file in 'w+' mode
    file_csv = open(path + 'data/skipped_demand.csv', 'w+', newline ='')
    
    # writing the data into the file
    with file_csv:    
        write = csv.writer(file_csv)
        write.writerows(skipped)

if __name__ == '__main__':
    get_demand_data()