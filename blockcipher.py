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


def BlockCipherDencrypt(k, c) :
    z = c^k
    for i in range(8) :
        for j in range(8) :
            Z[j] = (z >> 4*j) & (0x0000000f)
        Y[0] = Z[1] ^ Z[2] ^ Z[3] ^ Z[5] ^ Z[6] ^ Z[7]
        Y[1] = Z[0] ^ Z[2] ^ Z[3] ^ Z[4] ^ Z[6] ^ Z[7]
        Y[2] = Z[0] ^ Z[1] ^ Z[3] ^ Z[4] ^ Z[5] ^ Z[7]
        Y[3] = Z[0] ^ Z[1] ^ Z[2] ^ Z[4] ^ Z[5] ^ Z[6]
        Y[4] = Z[0] ^ Z[1] ^ Z[4] ^ Z[6] ^ Z[7]
        Y[5] = Z[1] ^ Z[2] ^ Z[4] ^ Z[5] ^ Z[7]
        Y[6] = Z[2] ^ Z[3] ^ Z[4] ^ Z[5] ^ Z[6]
        Y[7] = Z[0] ^ Z[3] ^ Z[5] ^ Z[6] ^ Z[7]
        for j in range(8) :
            X[j] = S.index(Y[j])
        x = 0x00000000
        for j in range(8) :
            x = x+(X[j] << 4*j) 
        z = x^k
    return z

    
P = 0x12345678
K = 0xC58FA10B
C = BlockCipherEncrypt(K, P)
print(hex(C))
print(hex(BlockCipherDencrypt(K, C)))
