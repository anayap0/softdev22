import imghdr 
import filetype


def validate_image(stream): # should support more than images. TODO: may remove 
    header = stream.read(512)
    stream.seek(0) 
    frmt = imghdr.what(None, header)
    if not frmt:
        return None
    return '.' + (frmt if frmt != 'jpeg' else 'jpg')




def validate_file(stream):
    header = stream.read(1000)
    stream.seek(0)
    kind = filetype.guess(header)
    print(kind.extension)
    if not kind:
        return None
    return '.' + (kind.extension if kind.extension != 'jpeg' else 'jpg') # the mime type (kind.mime) may be useful for later 
    
