import requests

s = requests.Session()
s.max_redirects = 100
s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
url = "https://www.caixa.gov.br/Downloads/sinapi-a-partir-jul-2009-sc/SINAPI_ref_Insumos_Composicoes_SC_202408_NaoDesonerado.zip"
# url = "https://www.riscos.info/packages/arm/Emulation/arcem_1.00-cvs-20110126-1.zip"
print(url)

r = s.get(url)
if r.status_code == 200:
    with open('sinapi.zip', 'wb') as f:
        f.write(r.content)

print(r.content)