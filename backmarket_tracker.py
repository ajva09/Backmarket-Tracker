#!/usr/bin/python3

'''
BackMarket price tracker and alerter
Set the 'price_wanted' and the 'false_positive_price' variables, see README for more informations
If you find any bugs, please report them under 'issues' in github

Note: Notify_run doesn't work with safari, for iOS devices, the next release will feature PushOver app support (https://pushover.net/) !

Made by 0xlazY !
'''

import requests, re
#from notify_run import Notify ## TODO

def get_currency(url):

    currency_dic = {
        '€': ['fr', 'es', 'it', 'de'],
        '$': ['com'],
        '£': ['uk'] ## co.uk
    }

    splited_url = url.split('.')
    
    if splited_url[3] == 'uk':
        splited_url = 'uk'
    else:
        splited_url = splited_url[2].split("/")[0]
    #print(splited_url) ## debug

    currency_symbole = "$" ## default, if failed
    
    for key, value in currency_dic.items():
        if splited_url in value:
            currency_symbole = key

    #print(currency_symbole) ##Debug
    return currency_symbole


def get_webcontent(url):

    page = requests.get(url)
    content = page.content.decode()
    currency_symbole = get_currency(url)

    pattern = 'price_with_currency.\".{0,9}.\"'
    raw_prices = re.findall(pattern, content) # Parse the entire WebPage, search 'price_with_currency*€'
    print(raw_prices) ## debug

    price_lst = []

    for price in raw_prices:
        try: # because of potential problems when loading webpages and inconsistency, use 'try' before any index reference ([.])
            if currency_symbole == '€':
                parsed_price = float(price.strip().split('"')[1].split('\xa0')[0].replace(',', '.')) # get rid of all the junk
            else:
                parsed_price = float(price.strip().split('"')[1].replace(currency_symbole, ''))

            if parsed_price > false_positive_price:
                price_lst.append(parsed_price) # add the formated price to the price_lst
        except:
            print("Problem ! {}".format(price))
    
    return price_lst


def alerter(price_lst):
    minimum_price = price_lst[0] # Initialize first minimum price

    for price in price_lst: # Gets the actual minimum price
        if price < minimum_price:
            minimum_price = price
    
    if minimum_price <= price_wanted:
        headers = {'Content-Type': 'text/text; charset=utf-8'} # needed to send specials char such as € ...
        data_text = '{}\'s price has drop to {}{} !'.format(device_name, minimum_price, currency_symbole)

        requests.post(notify_run_url, data = data_text.encode('utf-8'), headers = headers) # Send POST request to notidy_run channel

def get_notify_run_url(config_file):
    conf = open(config_file, 'r')
    conf_url = conf.readline().strip()
    conf.close()

    return conf_url



def main():
    for url in url_lst:
        #print(get_webcontent(url))
        price_lst = get_webcontent(url)
        #alerter(price_lst)g
        print(price_lst)


if __name__ == '__main__':
    url_lst = ['https://www.backmarket.fr/iphone-8-64-go-gris-sideral-debloque-tout-operateur-pas-cher/36827.html']
    device_name = 'iPhone X'
    # i.e, iPhone X 64gb Black

    currency_symbole = '$' # TODO add other currency support, $, £ ...

    notify_run_url = get_notify_run_url('config.cfg')
    # Create a notify_run channel and replace the url in config file (https://notify.run)
    ## TODO add channel creation with notidy_run module

    false_positive_price = 100 # Impossible price for the specified product
    price_wanted = 450 # Price of the product below which you want to receive a notification

    main()
    ##dev
