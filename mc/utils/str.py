

def human_readable_size(size) :
    size_unit = ['', 'K', 'M', 'G', 'T']
    i = 0
    try :
        size = int(size)
    except :
        return None

    while size >= 1024 and i < 5 :
        size = size / 1024
        i += 1

    return str(size) + size_unit[i]
