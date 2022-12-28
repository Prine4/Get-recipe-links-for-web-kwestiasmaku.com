import requests
from bs4 import BeautifulSoup


class Recepies:

    def __init__(self, keyword):
        self.keyword = keyword

    def crated_file(self, improve_list_of_links):
        del improve_list_of_links[1::2]

        file = open('output.txt', 'x')

        for ele in improve_list_of_links:
            file.writelines(ele+'\n')
        file.close

    def get_recepie_links(self, list_of_page_numbers):
        list_of_links = []
        bad_ele = '#'

        for page_number in list_of_page_numbers:

            str_page_number = str(page_number)

            r = requests.get('https://www.kwestiasmaku.com/szukaj?search_api_views_fulltext=' + self.keyword + '&page=' + str_page_number)
            soup = BeautifulSoup(r.content, 'html.parser')
            inside_page = soup.find('div', class_='view-content')

            for link in inside_page.find_all('a'):
                list_of_links.append(link.get('href'))

            while bad_ele in list_of_links:
                list_of_links.remove(bad_ele)

            for page_number in list_of_links:
                improve_list_of_links = ['https://www.kwestiasmaku.com/' + page_number for page_number in list_of_links]

        return improve_list_of_links

    def numbers(self):
        list_of_page_numbers = []

        for page_index in range(0, 100):

            page_number = str(page_index)

            r = requests.get('https://www.kwestiasmaku.com/szukaj?search_api_views_fulltext=' + self.keyword + '&page=' + page_number)
            soup = BeautifulSoup(r.content, 'html.parser')
            to_find_herf = soup.find('div', class_='text-center')
            for link in to_find_herf.find_all('a'):
                next_page = link.get_text('href')
            if next_page == 'dalej':
                list_of_page_numbers.append(page_number)
            else:
                break

        page_index = page_index + 1

        list_of_page_numbers.append(page_index - 1)

        return list_of_page_numbers


keyword = Recepies('placki')
keyword.crated_file(keyword.get_recepie_links(keyword.numbers()))
