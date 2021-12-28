import binascii
S = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7] #S(x) 함수
X = [0 for i in range(8)]
Y = [0 for i in range(8)]
Z = [0 for i in range(8)]


def BlockCipherEncrypt(k, p) :
    x = k^p 
    for i in range(8) :
        for j in range(8) :
            X[j] = (x >> 4*j) & (0x0000000f)
        for j in range(8) :
            Y[j] = S[X[j]]
        Z[0] = Y[0] ^ Y[2] ^ Y[3] ^ Y[5] ^ Y[6] ^ Y[7]
        Z[1] = Y[0] ^ Y[1] ^ Y[3] ^ Y[4] ^ Y[6] ^ Y[7]
        Z[2] = Y[0] ^ Y[1] ^ Y[2] ^ Y[4] ^ Y[5] ^ Y[7]
        Z[3] = Y[1] ^ Y[2] ^ Y[3] ^ Y[4] ^ Y[5] ^ Y[6]
        Z[4] = Y[0] ^ Y[1] ^ Y[5] ^ Y[6] ^ Y[7]        
        Z[5] = Y[1] ^ Y[2] ^ Y[4] ^ Y[6] ^ Y[7]        
        Z[6] = Y[2] ^ Y[3] ^ Y[4] ^ Y[5] ^ Y[7]        
        Z[7] = Y[0] ^ Y[3] ^ Y[4] ^ Y[5] ^ Y[6]        
        z = 0x00000000
        for j in range(8) :
            z = z+(Z[j] << 4*j)
        x = z^k
    return x


def MD_strengthening_padding(msg) :
    M = []
    padded_msg = msg + b'8'
    times = 7 - ((len(msg)+4) % 8)
    for i in range(times) :
        padded_msg = padded_msg + b'0'
    padded_msg = padded_msg + str(hex(len(msg)*4)).encode('utf8')[2:].zfill(4)
    for i in range(0, len(padded_msg), 8) :
        M.append(int(str(padded_msg[i:i+8])[2:10], 16))
    return M

def hash(message) :
    x = 0xa5c8f1ee #IV
    if type(message) == str :
        message = binascii.hexlify(message.encode('utf8'))
    else: 
        message = str(hex(message)).encode('utf8')[2:]
    M = MD_strengthening_padding(message)
    for i in range(len(M)) :
        x = BlockCipherEncrypt(M[i], x) ^ x
    return x


p = 521
q = 613
n = p*q
e = 11
def phi(p, q) :
    return (p-1)*(q-1)

def EEA(a, b) :
    (old_r, r) = (a, b)
    (old_s, s) = (1, 0)
    (old_t, t) = (0, 1)

    while r != 0 :
        quotient = old_r // r
        (old_r, r) = (r, old_r - quotient * r)
        (old_s, s) = (s, old_s - quotient * s)
        (old_t, t) = (t, old_t - quotient * t)
    return old_s

def exp_mod(a, k, n) :
    answer = 1
    while k != 0 :
        if k&1 == 1 :
            answer = (answer*a) % n
        k = k >> 1
        a = (a*a) % n
    return answer

d = EEA(e, phi(p, q)) % phi(p, q)


def Encryption(m) :
    return exp_mod(m, e, n) 
def Decryption(c) :
    return exp_mod(c, d, n) 


def digital_signature(msg) :
    return Decryption(hash(msg))
def verify (msg, s) :
    if Encryption(s)==(hash(msg) % n) : 
        return True
    else : 
        return False



message = "Twinkle twinkle little star How I wonder what you are Up above the world so high Like a diamond in the sky Twinkle twinkle little star How I wonder what you are"

print("서명 값(s) :",digital_signature(message))
print(verify(message, digital_signature(message)))

