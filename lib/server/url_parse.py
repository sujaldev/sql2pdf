def percent_decode(string):
    percent_map = {
        "+": " ",
        "%0D": "",
        "%0A": "\n",
        "%20": " ",
        "%21": "!",
        "%22": '"',
        "%23": "#",
        "%24": "$",
        "%25": "%",
        "%26": "&",
        "%27": "'",
        "%28": "(",
        "%29": ")",
        "%2A": "*",
        "%2B": "+",
        "%2C": ",",
        "%2F": "/",
        "%3A": ":",
        "%3B": ";",
        "%3D": "=",
        "%3F": "?",
        "%40": "@",
        "%5B": "[",
        "%5D": "]"
    }
    for encoded, decoded in percent_map.items():
        string = string.replace(encoded, decoded)
    return string


def extract_params(last_dir):
    key_val_url = {}
    if "?" in last_dir:
        data = last_dir.split("?")
        end_dir = data[0]
        params = data[1]
        if "&" not in params:
            print("multiple parameters in url found")
            params = params.split("=")
            key_val_url[percent_decode(params[0])] = percent_decode(params[1])
        else:
            params = params.split("&")
            for param in params:
                get_data = param.split("=")
                key_val_url[percent_decode(get_data[0])] = percent_decode(get_data[1])
        return end_dir, key_val_url
    else:
        return last_dir, key_val_url


def parse_url(url):
    data = url.split("/")
    param_data = extract_params(data[-1])
    data[-1] = param_data[0]
    get_params = param_data[1]
    return data, get_params
