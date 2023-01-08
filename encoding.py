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
        sub = fpes + enc + mvws
        haystack = haystack.replace(' ', sub, 1)
        last = i + len(sub)
    return haystack

def encode_word(word: str) -> str:
    ascii = [bin(x)[2:].rjust(8, '0') for x in bytearray(word, 'ascii', errors='backslashreplace')]
    return ''.join(ascii).replace('0', zwnj).replace('1', zwj)

def decode(ct: str) -> str:
    ot = ''
    last = 0
    while True:
        try:
            start = ct.index(fpes, last)
        except ValueError:
            break
        end = ct.index(mvws, start)
        if last != 0:
            ot += ' '
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
    bash_corpus = 'Bash  is  an sh-compatible command language interpreter that executes commands read from the standard input or from a file.  Bash also incorporates useful features from the Korn and C shells (ksh and csh).'
    ot1 = 'bsy'
    ct1 = encode(bash_corpus, ot1)
    print(decode(ct1) == ot1)

    ot2 = 'BSY seems like a good subject to study at FEE.'
    ct2 = encode(bash_corpus, ot2)
    print(decode(ct2) == ot2)

    ot3 = 'hehehe 😂'
    ct3 = encode(bash_corpus, ot3)
    print('hehehe' in decode(ct3))
    print('\\U0001f602' in decode(ct3))
