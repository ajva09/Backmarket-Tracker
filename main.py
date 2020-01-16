import subprocess
from py_pushover_simple import pushover

#gris_url = 'https://www.backmarket.fr/iphone-x-64-go-gris-sideral-debloque-tout-operateur-pas-cher/36833.html'
#blanc_url = 'https://www.backmarket.fr/iphone-x-64-go-argent-debloque-tout-operateur-pas-cher/36835.html'

#cmd_gris = 'curl -s https://www.backmarket.fr/iphone-x-64-go-gris-sideral-debloque-tout-operateur-pas-cher/36833.html | grep -E -o "price_with_currency.\".{0,6}"'   
#cmd_blanc = 'curl -s https://www.backmarket.fr/iphone-x-64-go-argent-debloque-tout-operateur-pas-cher/36835.html | grep -E -o "price_with_currency.\".{0,6}"'

script_name = 'test.sh'
price_wanted = 400

def get_data(script_name):

    raw_gris = subprocess.run(['bash', script_name], stdout=subprocess.PIPE)

    raw_content = raw_gris.stdout.decode(errors='ignore')
    raw_content = raw_content.strip().split("END")

    gris_raw = raw_content[0].split("\n")
    blanc_raw = raw_content[1].split("\n")

    gris_data = []
    blanc_data = []

    for line in gris_raw:
        try:
            prix = float(line.split('"')[1].strip().replace(',', '.'))
            if prix > 150:
                gris_data.append(prix)
        except:
            pass

    for line in blanc_raw:
        try:
            prix = float(line.split('"')[1].strip().replace(',', '.'))
            if prix > 150:
                blanc_data.append(prix)
        except:
            pass
    
    return gris_data, blanc_data


def send_message(message):
    p = pushover.Pushover()
    p.user = 'uw1cvkzwh654zzuxwrm9z1xt39mq7u'
    p.token = 'a41uj3muckxwqvt6bhap4jcajd38a1'

    p.sendMessage(message)


def notify(data):
    for i in range(len(data)):
        if i == 0:
            couleur = 'Gris'
        else:
            couleur = 'Argent'

        for prix in data[i]:
            if prix <= price_wanted:
                send_message('iPhone X {} au prix de {} € !!'.format(couleur, prix))



if __name__ == '__main__':
    data = get_data(script_name)
    #print(data)
    notify(data)