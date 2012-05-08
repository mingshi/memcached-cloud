

def human_readable_size(size) :
    size_unit = ['B', 'K', 'M', 'G', 'T']
    i = 0
    try :
        size = float(size)
    except :
        return None

    while size >= 1024 and i < 5 :
        size = size / 1024
        i += 1

    return str(round(size, 2)) + size_unit[i]
