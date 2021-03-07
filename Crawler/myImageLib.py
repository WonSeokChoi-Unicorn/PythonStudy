import io
import struct
import urllib.request as urllib2


def getImageInfo(imgUrl):
    req = urllib2.Request(imgUrl, headers={"Range": "5000", "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"})

    # 오류 발생시 빈 값 리턴
    try:
        r = urllib2.urlopen(req)
    except:
        print("URL Open Error")
        return "", "", ""
    
    data = r.read()

    size = len(data)
    # print(size)
    height = -1
    width = -1
    content_type = ''

    # handle GIFs
    if (size >= 10) and data[:6] in (b'GIF87a', b'GIF89a'):
        # Check to see if content_type is correct
        content_type = 'image/gif'
        w, h = struct.unpack(b"<HH", data[6:10])
        width = int(w)
        height = int(h)

    # See PNG 2. Edition spec (http://www.w3.org/TR/PNG/)
    # Bytes 0-7 are below, 4-byte chunk length, then 'IHDR'
    # and finally the 4-byte width, height
    elif ((size >= 24) and data.startswith(b'\211PNG\r\n\032\n')
            and (data[12:16] == b'IHDR')):
        content_type = 'image/png'
        w, h = struct.unpack(b">LL", data[16:24])
        width = int(w)
        height = int(h)

    # Maybe this is for an older PNG version.
    elif (size >= 16) and data.startswith(b'\211PNG\r\n\032\n'):
        # Check to see if we have the right content type
        content_type = 'image/png'
        w, h = struct.unpack(b">LL", data[8:16])
        width = int(w)
        height = int(h)

    # handle JPEGs
    elif (size >= 2) and data.startswith(b'\377\330'):
        content_type = 'image/jpeg'
        jpeg = io.BytesIO(data)
        jpeg.read(2)
        b = jpeg.read(1)
        try:
            while (b and ord(b) != 0xDA):
                while (ord(b) != 0xFF): b = jpeg.read(1)
                while (ord(b) == 0xFF): b = jpeg.read(1)
                if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                    jpeg.read(3)
                    h, w = struct.unpack(b">HH", jpeg.read(4))
                    break
                else:
                    jpeg.read(int(struct.unpack(b">H", jpeg.read(2))[0])-2)
                b = jpeg.read(1)
            width = int(w)
            height = int(h)
        except struct.error:
            pass
        except ValueError:
            pass

    return content_type, width, height

# imageUrl = "https://t1.daumcdn.net/thumb/R1024x0/?fname=https://cdn.ggoorr.net/files/attach/images/124/189/857/010/62d18a473136c68ecd81ea665d57db8f.jpg"
# imageUrl = "https://t1.daumcdn.net/cfile/tistory/9924734F5AE03D2729?original"
# imageUrl = "https://cdn.ggoorr.net/files/attach/images/124/189/857/010/7ce4a5dd1a74b5bd506426424aab3830.jpg"
# imageUrl = "https://img1.daumcdn.net/thumb/R1024x0/?fname=https://t1.daumcdn.net/cafeattach/aVeZ/edb3e6d61a36efa1320dd8c0a12ad7ab850cd937"
# imageUrl = "http://img.vogue.co.kr/vogue/2021/02/style_602f192d49503-1122x1400.jpg"
imageUrl = "https://1.bp.blogspot.com/-vF3httpOv6I/YC2TYrnrBfI/AAAAAAAAjG8/zRNq4MXLHEAtwQNkNKb7WZY1MqX9yPZgQCLcBGAsYHQ/s0/07.jpg"

print(getImageInfo(imageUrl))
