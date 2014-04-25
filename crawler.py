__author__ = 'Dan'

# from sample_input import sample_html
from bs4 import BeautifulSoup
import urllib2
import requests
import json

# soup = BeautifulSoup(sample_html)


def get_faculty(soup_input):
    """Gets every row for a faculty member"""
    faculty_list = []
    for tr in soup_input.find_all('tr'):
        td = tr.find_all('td')
        if len(td) > 0:
            if td[4].get_text() == 'Faculty':
                faculty_list.append(td)
    return faculty_list


def get_links(faculty_list):
    """Gets link to web page for every faculty"""
    links_list = []
    for entry in faculty_list:
        # print entry[0]
        link = entry[1].find('a').get('href')
        links_list.append(link)
    return links_list


def get_html(links):
    """Get html code for a faculty web page"""
    faculty_htmls = []
    limit = 10;
    if len(links) < 10:
        limit = len(links)
    for i in range(0, limit):  # Only process first 5 because processing all is too long
        usock = urllib2.urlopen(links[i])
        data = usock.read()
        usock.close()
        faculty_htmls.append(data)
    return faculty_htmls

def get_info(html_file):
    """Get required info for each faculty"""

    info = {'name': None, 'id': None, 'classification': None, 'title': None, 'dept': None, 'dept_code': None,
            'email': None, 'phone': None, 'address': None}

    soup2 = BeautifulSoup(html_file)

    name = soup2.find('td').find('b').get_text()
    info['name'] = name

    tr = soup2.find_all('tr')
    for row in tr:
        td = row.find_all('td')
        title = td[0].get_text()
        if title == 'UVa Computing ID':
            info['id'] = td[1].get_text()
        elif title == 'Classification':
            info['classification'] = td[1].get_text()
        elif title == 'Title':
            info['title'] = td[1].get_text()
        elif title == 'Department':
            info['dept'] = td[1].get_text()
        elif title == 'Department Code':
            info['dept_code'] = td[1].get_text()
        elif title == 'Primary E-Mail Address':
            info['email'] = td[1].get_text()
        elif title == 'Office Phone':
            info['phone'] = td[1].get_text()
        elif title == 'Office Address':
            info['address'] = td[1].get_text()
    return info


def post_request(search_entry):
    """Send POST request to search page"""
    payload = {'whitepages': search_entry}
    r = requests.post('http://www.virginia.edu/cgi-local/ldapweb', data=payload)
    html_src = r.text
    return html_src


def process_search(search_entry):
    """Processes a search entry, this should be the only function that is called externally"""
    # html_page = post_request(search_entry) # get HTML for request
    # soup3 = BeautifulSoup(html_page) # make BeautifulSoup object
    soup3 = BeautifulSoup(search_entry)
    check = soup3.find('br').find('h3') # check to see if result(s) is returned

    data = {}  # list for results

    if check is None:  # if result returned
        check2 = soup3.find('table').find('tr').get_text()  # check if specific result returned or list
        if check2 == 'Directory Search Results':  # if list of results returned
            fac = get_faculty(soup3)
            links_list = get_links(fac)
            html_list = get_html(links_list)
            for fac in html_list:
                x = get_info(fac)
                data[x['name'].split('(')[0][:-1]] = x
                # print x
            return json.dumps(data, indent=4)
        else:  # individual result returned
            x = get_info(search_entry)
            data[x['name'].split('(')[0][:-1]] = x
            # print x
            return json.dumps(data, indent=4)
    else:  # else there was error, none found, or too many entries
        # print None
        return json.dumps(data, indent=4)

# if __name__ == "__main__":
#     x = process_search(sample_html) #example if we search 'evans'
#     print json.dumps(x, indent=4)
