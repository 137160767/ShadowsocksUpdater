import requests
from lxml import html
import json

headers={
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
'accept-language':'zh-cn'}

ip_url='https://ip.cn'
page=requests.get(ip_url,headers=headers)
selector = html.fromstring(page.text)
ip_address=selector.xpath('//*[@id="result"]/div/p[1]/code/text()')[0]
phy_address=selector.xpath('//*[@id="result"]/div/p[2]/code/text()')[0]

session = requests.Session()

with open('config.json', 'r') as f:
    data = json.load(f)
page=session.post('https://portal.shadowsocks.to/dologin.php',data=data,headers=headers)
cookies=page.cookies

page=session.get('https://portal.shadowsocks.to/clientarea.php',cookies=cookies,headers=headers)
cookies=page.cookies

selector = html.fromstring(page.text)
product_link='https://portal.shadowsocks.to'+(selector.xpath('//*[@id="main-body"]/div/div/div[3]/div[2]/div/div[1]/div[1]/div[2]/a/@href')[0])

page=session.get(product_link,cookies=cookies,headers=headers)
selector = html.fromstring(page.text)

left_traffic=selector.xpath('//*[@id="manage"]/div/div[1]/div[2]/table/tbody/tr[6]/td[2]/center/text()')[0]

print(left_traffic)

config_path='C://Users//Jiutong Zhao//Desktop//'

with open(config_path+'gui-config.json', 'r') as f:
    data = json.load(f)

data['configs'][-1]['remarks']='剩余流量:%s,本机IP:%s'%(left_traffic,ip_address)
data['configs'][-1]['server']=phy_address
data['configs'][-1]['server_port']='0'

with open('C://Users//Jiutong Zhao//Desktop//gui-config.json', 'w') as f:
    json.dump(data, f)
