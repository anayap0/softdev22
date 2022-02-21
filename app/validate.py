
import imghdr 


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0) 
    frmt = imghdr.what(None, header)
    if not frmt:
        return None
    return '.' + (frmt if frmt != 'jpeg' else 'jpg')