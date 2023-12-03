# import required  modules
import urllib.request
from calendar import monthrange
import calendar

#Year list function
def year_lst(year_start = 2023, year_end = 2023):
    # Year list preparation
    year = list(range(year_start, year_end+1 ,1))
    year_lst = []
    for y in year:
        year_name = str(y) + "-" + str(y+1)
        year_lst.append(year_name)
    return year_lst, year

# Function to download pdf files
def url_def(month_no,y, path):
    for m in month_no:
        if(m<=3):
            i=y-1
        else:
            i=y
        month_name = calendar.month_name[m]
        url = 'https://report.grid-india.in/ReportData/Daily%20Report/PSP%20Report/'+str(i)+'-'+str(i+1)+'/'+month_name+'%20'+str(y)+'/'
        _, no_of_days = monthrange(i, m)
        for d in range(1,no_of_days+1):
            if (d<10):
                day_no = '0'+str(d)
            else:
                day_no = str(d)
            if (m<10):
                month_no = '0'+str(m)
            else:
                month_no = str(m)
            filename = day_no + '.' + month_no + '.' + str(y)[-2:] + '_NLDC_PSP.pdf'
            url_full = url + filename
            print(url_full)
            try:
                urllib.request.urlretrieve(url_full, path + "Dailydata/"+filename)
            except:
                
                pass

# Main function to download data
def download_data(start_year, end_year, path):
    _, year = year_lst(start_year, end_year)
    for i in year:
        print(i)
        if i == end_year:
            month_no = list(range(4,11))
            url_def(month_no,i, path)
        elif i!= start_year:
            month_no = list(range(4,13))
            url_def(month_no,i, path)
            month_nxt = list(range(1,4))
            url_def(month_nxt,i+1, path)
        elif i==start_year:
            month_nxt = list(range(1,4))
            url_def(month_nxt,i+1, path)

# if __name__ == '__main__':
#     download_data(2023,2023)
