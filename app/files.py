import filetype

def validate_file(stream):
    header = stream.read(1000)
    stream.seek(0)
    kind = filetype.guess(header)
    print(kind.extension)
    if not kind:
        return None
    return '.' + (kind.extension if kind.extension != 'jpeg' else 'jpg') # the mime type (kind.mime) may be useful for later 
    
