import requests
from datetime import datetime
from bs4 import BeautifulSoup


class ParseExchenge:
    @classmethod
    def get_html(cls, url, useragent=None, proxy=None):
        r = requests.get(url, headers=useragent, proxies=proxy, verify=False)
        return r.text

    @classmethod
    def get_target_html(cls):
        host = 'https://bai.kz'
        url = '{}/kursy/almaty/'.format(host)
        return cls.get_html(url)

    @classmethod
    def get_beautiful_data(cls):
        html = cls.get_target_html()

        soup = BeautifulSoup(html, 'lxml')
        banks = soup.find('div', class_='subsection'). \
            find('table', class_='banks_table').find_all('tr', recursive=False)

        if banks:
            return banks
        return None

    @classmethod
    def get_data_from_tag(cls, tag):
        tag_data = []
        bank_name = tag.find('div', class_="t_bank_name")
        bank_name = None if bank_name is None else bank_name.text.strip()
        if bank_name is None:
            br = tag.find('br')
            if br is not None:
                bank_name = br.previous_sibling.strip()
            else:
                bank_name = 'None'

        bank_dir = tag.find('td', class_="bank_dir_table")
        if bank_dir is not None:
            money_type = bank_dir.find('tr', class_="rate-result")
            money_type = '' if money_type is None else money_type.find('strong').text.strip()

            trs = bank_dir.find_all('tr')
            for tr in trs[1:]:
                tds = tr.find_all('td')
                buy = tds[0].text.strip()
                buy = 0 if buy == '-' else buy
                currency_name = tds[1].text.strip()
                sale = tds[2].text.strip()
                sale = 0 if sale == '-' else sale
                bank_data = {
                    'handler_name': bank_name,
                    'money_type': money_type,
                    'name': currency_name,
                    'buy': buy,
                    'sale': sale
                }
                if bank_data['money_type'] == 'наличные':
                    tag_data.append(bank_data)
        return tag_data

    @classmethod
    def start_parse(cls):
        tbody = cls.get_beautiful_data()
        if tbody is None:
            return

        data = []
        for tag in tbody[2:]:
            tag_data = cls.get_data_from_tag(tag)
            data.extend(tag_data)

        return data
        # save_to_textfile(data)



