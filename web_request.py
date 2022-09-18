#Create a pem certificate for the request to use
import ssl
import urllib.request

_context = ssl.create_default_context()
_context.check_hostname = False
_context.verify_mode = ssl.CERT_NONE

def Get_Webpage(URL:str):
    with urllib.request.urlopen(URL, context=_context) as response:
        return response.read()