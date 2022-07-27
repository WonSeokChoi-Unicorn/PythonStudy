# Cloudflare-protected Email 복호화
def deCFEmail(cfemail):
    try:
        r = int(cfemail[:2],16)
        email = ''.join([chr(int(cfemail[i:i+2], 16) ^ r) for i in range(2, len(cfemail), 2)])
        return email
    except (ValueError):
        pass

print(deCFEmail("543931142127353935313e352e7a373b39"))