zwnj = u'\u200c'
zwj = u'\u200d'
fpes = u'\u2005'
mvws = u'\u180e'

def encode(haystack: str, needle: str) -> str:
    split = needle.split(' ')
    last = 0
    for word in split:
        i = haystack.index(' ', last)
        enc = encode_word(word)
        haystack = haystack.replace(' ', enc, 1)
        last = i + len(enc)
    return haystack

def encode_word(word: str) -> str:
    ascii = ''
    for c in word:
        n = ord(c)
        b = bin(n)[2:].rjust(8, '0')
        ascii += b
    return fpes + ascii.replace('0', zwnj).replace('1', zwj) + mvws

def decode(ct: str) -> str:
    ot = ''
    last = 0
    while True:
        try:
            start = ct.index(fpes, last)
        except ValueError:
            break
        end = ct.index(mvws, start)
        ot += decode_word(ct[start+1:end])
        last = end
    return ot
    
def decode_word(ct: str) -> str:
    l = len(ct)
    i = 0
    ot = ''
    while i + 8 <= l:
        block = ct[i:i+8]
        ascii = block.replace(zwnj, '0').replace(zwj, '1')
        ot += chr(int(ascii, 2))
        i += 8
    return ot

if __name__ == '__main__':
    res = encode('Bash  is  an sh-compatible command language interpreter that executes commands read from the standard input or from a file.  Bash also incorporates useful features from the Korn and C shells (ksh and csh).', 'bsy')
    print(res)
    o = decode(res)
    print(o)
    print(o == 'bsy')
