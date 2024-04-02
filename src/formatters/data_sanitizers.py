def sanitize_data(data, data_type):
    '''
    Sanitizes input based on data type.
    \nint defaults to 0
    \nfloat defaults to 0.0
    \nstring defaults to ""
    '''    
    if data_type is str:
        return strip_characters(data) if(data) else ""
    elif data_type is int or data_type is float:
        try:
            return float(str(data)) if data_type is float else int(str(data)) if data_type is int else 0
        except:
            return 0.0 if data_type is float else 0
    else:
        return data
    
def strip_characters(data):
    try:
        return data.replace('\0x00', '').replace('\0xe3', '').replace('\0', '').strip()
    except:
        print(f'"{data}" is not a string')