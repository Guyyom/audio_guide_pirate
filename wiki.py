import requests

def nested_dict_pairs_iterator(dict_obj):
    # Iterate over all key-value pairs of dict argument
    for key, value in dict_obj.items():
        # Check if value is of dict type
        if isinstance(value, dict):
            # If value is dict then iterate over all its values
            for pair in nested_dict_pairs_iterator(value):
                yield (key, *pair)
        else:
            # If value is not dict type then yield the value
            yield (key, value)

def request_api(lang, input):
    #API Request through Wiki TextExtracts API
    s = requests.Session()
    url = "https://" + lang + ".wikipedia.org/w/api.php"
    params = {
        #Action Query is the TextExtracts API
        'action': 'query',
        'format': 'json',
        'titles': input,
        'prop': 'extracts',
        'exintro': True,
        'explaintext': True,
        }

    #Retrieve the response
    r = s.get(url=url, params=params)
    if not r: 
        return False
    else: 
        data = r.json()
        #Loop through all key-value pairs of a nested dictionary
        for pair in nested_dict_pairs_iterator(data):
            if 'extract' in pair:
                index = pair.index('extract')
                tts = pair[index+1]
                wikiid = pair[2]
                return tts, wikiid

