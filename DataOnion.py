import requests
import html
import base64
import binascii

def nextStep(data):
    if type(data) == str:
        f = bytearray(data, encoding='utf8')
    else:
        f = bytearray(data)
    f = f.split(b'<~')[1]
    f = f.split(b'~>')[0]
    #print(f.decode('utf-8'))
    f = f.replace(b'\n',b'')
    f = base64.a85decode(b'<~' + f + b'~>', adobe=True)
    return f



f = requests.get('https://www.tomdalling.com/toms-data-onion/')
f = nextStep(html.unescape(f.text))

hexo = binascii.hexlify(f[0:120])
print(hexo)
print(f.decode('utf-8'))

f = nextStep(f)



back = bytearray()
for e in f:
    temp = e ^ 0x55
    if (temp & 0x01):
        back.append(temp // 2 + 128)
    else:
        back.append(temp // 2)
f = back

hexo = binascii.hexlify(f[0:120])
print(hexo)
print(f.decode('utf-8'))

f = nextStep(f)


back = bytearray()
count = 0
temp = 0
for e in f:
    bits = 0
    tempVal = e
    while e != 0:
        if e & 0x01:
            bits += 1 
        e >>= 1
    if (0 == bits % 2): 
        # 7 bits correct
        temp <<= 7
        temp += (tempVal & 0xfe)>>1
        count += 1
        if count == 8:
            # 7 bytes finished
            count = 0
            for i in range(7):
                tempByte = (temp&(0xff<<(6*8)))>>(6*8)
                back.append(tempByte)
                temp <<= 8
            temp = 0
f = back

hexo = binascii.hexlify(f[0:120])
print(hexo)
print(f.decode('utf-8'))
















