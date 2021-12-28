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


def Encryption(m, e, n) :
    return exp_mod(m, e, n) 
def Decryption(c, d, n) :
    return exp_mod(c, d, n) 

M_1 = 150000
C_2 = 272301

print("Private key :", d)
print("C_1 :", Encryption(M_1, e, n))
print("M_2 :", Decryption(C_2, d, n))
