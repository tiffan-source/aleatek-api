def convert_to_dict(obj):
    result = {}

    for key, value in obj.items():
        if '[' in key and ']' in key:
            keys = key.split('[')
            keys = [k.strip(']') for k in keys if k.strip(']') != '']
            current_dict = result

            for i, k in enumerate(keys):
                if k not in current_dict:
                    current_dict[k] = {}

                if i == len(keys) - 1:
                    current_dict[k] = value
                else:
                    current_dict = current_dict[k]
        else:
            result[key] = value

    return result