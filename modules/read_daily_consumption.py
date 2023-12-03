# importing required modules
import PyPDF2
import pandas as pd
import glob 

def get_daily_consumption(path):
    files = glob.glob(path + 'Weeklydata/*.pdf',  
                    recursive = True) 
    df_new = pd.DataFrame()
    for file in files:
        file = file.replace('\\','/') 
        print(file)  
    
        # creating a pdf file object
        pdfFileObj = open(file, 'rb')
        
        # creating a pdf reader object
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        
        # printing number of pages in pdf file
        #print(len(pdfReader.pages))
        
        # creating a page object
        check_first_page = pdfReader.pages[0]
        if check_first_page.extract_text() == "":
            page_no = 3
        elif check_first_page.extract_text().find("National Load Despatch Centre") != -1:
            page_no = 3
        else:
            page_no=2
        
        pageObj = pdfReader.pages[page_no]
        
        # extracting text from page
        #print("Page 1")
        #print(type(pageObj))
        str_pg = pageObj.extract_text()
        #print(pageObj.extract_text())

        #print(lst_pg)
        index_rep = str_pg.find('Region States')
        if(index_rep == -1):
            index_rep = str_pg.find('RegionStates') 
        str_pg = str_pg.replace(str_pg[:index_rep],"")
        unw_lst = ['ISTS*', 'ISTS', '(UT)','*']
        for i in unw_lst:
            str_pg = str_pg.replace(i,"")
        
        from_replace=['Region States', 'Essar steel', 'Andhra Pradesh', 'Tamil Nadu', 'West Bengal', 'Arunachal Pradesh']
        to_Replace = []
        for i in from_replace:
            new_txt = i.replace(' ','')
            #print(new_txt)
            str_pg = str_pg.replace(i,new_txt)

        lst_pg = str_pg.splitlines()
        total_lst= []
        for i in lst_pg:
            total_lst.append(i.split())
        # for i in total_lst[1]:
        #     print(i)
        #     print(type(i))

        #print(total_lst)
        total_lst = total_lst[:-5]
        #print(total_lst)
        
        # Create the pandas DataFrame 
        df = pd.DataFrame(total_lst) 
        
        # print dataframe. 
        df.reset_index(drop=True, inplace=True)
        df.columns=df.iloc[0]
        df = df.drop([0])

        #Create the index 
        index_ = df['RegionStates'] 
        
        # Set the index 
        df.index = index_ 
        
        # Print the DataFrame 
        #print(df) 

        # return the transpose 
        df = df.drop(['RegionStates'], axis=1)
        result = df.transpose() 
        
        # Print the result 
        #print(result)

        df_new = pd.concat([df_new, result])
        
        
        # closing the pdf file object
        pdfFileObj.close()

    df_new.to_csv("data/Energy_Consumption_data_2018_2023.csv")