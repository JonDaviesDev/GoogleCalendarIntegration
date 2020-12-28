from datetime import datetime
import requests, bs4, csv, pandas, re, sys, os

def clean_data(data):

    index = 0
    data_list_format = []

    for x in data:
       
        x = x.replace('\n', '', 1)      # removes the first instance of '\n'
        x = x.replace('\n', ',', 3)     # replaces the next three '\n' with ','
        
        if index != 0:                  # if iteration is not on the first element (column names)
            x = x.replace(',', '', 2)   # remove the first 2 ','
            x = x.partition(' ')[2]     # remove everything before the first space (' ')
            x_date = x.split(',')[0]
            formatted_date = datetime.strptime(x_date, '%d %B %Y')
            x = x.replace(x.split(',')[0], formatted_date.strftime('%d-%m-%Y'))
        

        data_list_format.append(x)
        index += 1

    return data_list_format

def generate_filename(start_date, end_date):
    start_date_modified = start_date.split(',')[0]
    end_date_modified = end_date.split(',')[0]

    return str(str(index) + '_STT___' + start_date_modified + '_to_' + end_date_modified + '.csv') # STT = Swansea Tide Times

def get_last_page_number(url):
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        page = bs4.BeautifulSoup(response.text)
        target = page.select('li')
        data = [element.getText() for element in target]
    else:
        sys.exit()

    return int(data[data.index('…') + 1])

def create_directory(path, directory_name):

    if os.path.exists(directory_name):
        pass
    else:
        directory_path = str(path + '\\' + directory_name)

        try:
            os.mkdir(directory_path)
        except OSError:
            print ("Creation of the directory %s failed" % directory_path)
        else:
            print ("Successfully created the directory %s " % directory_path)


starting_url = 'https://www.gowerlive.co.uk/swansea-tide-times/'
webpage_limit = get_last_page_number(starting_url)       # This is the number of pages to search (indicated at the bottom of the webpage)
index = 1
directory_name = 'TideTimes'
create_directory(os.getcwd(), directory_name)


for webpages in range(webpage_limit):

    if index == 1:
        response = requests.get(starting_url)
    else:
        response = requests.get(str(starting_url + 'page/' + str(index) + '/'))

    if response.status_code == requests.codes.ok:

        page = bs4.BeautifulSoup(response.text, features="html.parser")
        target = page.select('tr')
        data = [element.getText() for element in target]
        data = clean_data(data)

        data_start_and_end = data[1], data[-1]    

        with open(str(directory_name + '\\' + generate_filename(data_start_and_end[0], data_start_and_end[1])), 'w') as f:
            for element in data:
                f.write("%s" % element)
    else:
        sys.exit()

    index += 1
    
print('Process completed!')






