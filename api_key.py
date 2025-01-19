def get_api_key():
    with open('api_key.txt', 'r') as f:
        api_key = f.read()
    return api_key