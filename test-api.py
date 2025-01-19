import requests

def get_google_response(url):
    
    print('Trying to get a response from ' + url)
    try:
        response = requests.get(url)
        
    except:
        print('Something went wrong')
        
    else:
        print('Response code: ' + str(response.status_code))


URL = ['https://www.google.com','http://www.google.com1']

for url in URL:
    get_google_response(url)
    print('')
