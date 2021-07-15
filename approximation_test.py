import numpy as np

def generate_approximation(sbox_):
    """generate full bias from S-box"""
    approx = np.zeros((16,16))
    for x in range(16):
        for y in range(16):
            count = 0
            for i in range(16):
                a =  i&x ^ sbox_[i]&y
                f = 0
                while a > 0:
                    f ^= a & 1
                    a >>= 1
                if f !=0:
                    count += 1
            approx[x,y] = abs((count - 8)/16)
            
    return approx

def bit_sum(a):
    """Return the sum of set bit in a binary (e.g. bit_sum(0101) = 2)"""
    f = 0
    while a > 0:
        f += a & 1
        a >>= 1
    return f

def getbit(n,i):
    """Helper method for pbox_enc()"""
    return (n >> i) & 1

def setbit(n,i,v):
    """Helper method for pbox_enc()"""
    if (v == 1):
        n |= (1 << i)
    else:
        n &= ~(1 << i)
	
    return n


def pbox_enc(inp):
    """Perform P-box permutation on 16-bit binary
    input: 16-bit binary
    output: 16-bit binary
    """
    out = 0
    for i in range(16):
        if(getbit(inp,i)):
            out = setbit(out,pbox[i],1)
    return out

pbox = [0,4,8,12,1,5,9,13,2,6,10,14,3,7,11,15]  
sbox = [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7]  
APPROXIMATION = generate_approximation(sbox)
#print(APPROXIMATION)

def calculate_approximation(u,v):
    """Calculate bias approximation using Pilling-up Lemma
    input: 16-bit binary of round input U and output V
    output: Bias approximation 
    
    Example:
        input:
            U = 0000 0100 0000 0100
            V = 0000 0101 0000 0101
        output:
            bias = 2 * 0.25 * 0.25 = 0.125 
    """
    bias = 1
    for i in range(0,16,4):
        block_u = u>>i & 0b1111
        block_v = v>>i & 0b1111
        if block_u != 0 and block_v != 0:
            bias *= 2 * APPROXIMATION[block_u,block_v]
    return bias/2

possible_output = [[0], [1], [2], [1, 2, 3], [4], [1, 4, 5], [2, 4, 6], [1, 2, 3, 4, 5, 6, 7], [8], [1, 8, 9], [2, 8, 10], [1, 2, 3, 8, 9, 10, 11], [4, 8, 12], [1, 4, 5, 8, 9, 12, 13], [2, 4, 6, 8, 10, 12, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]]

def mask(n,i,j,k,l):
    """Convert S-box positions into binary mask
        input: n - 4-bit S-box position (e.g 0101) 
               i,j,k,l - 4-bit component of each S-box
        output: 16-bit mask of S-box
        
    Example:
        input: n = 0101, i = 0111, j = 0101, k = 0000, l = 0000
        output: 0000 0111 0000 0101
    """
    if (n == 0b0000):
        return 0;
    elif (n == 0b0001):
        return i;
    elif (n == 0b0010): 
        return i << 4;
    elif (n == 0b0011):
        return i << 4 ^ j; 
    elif (n == 0b0100):
        return i << 8;
    elif (n == 0b0101):
        return i << 8 ^ j;
    elif (n == 0b0110):
        return i << 8 ^ j << 4;
    elif (n == 0b0111):
        return i << 8 ^ j << 4 ^ k;
    elif (n == 0b1000):
        return i << 12;
    elif (n == 0b1001):
        return i << 12 ^ j;
    elif (n == 0b1010):
        return i << 12 ^ j << 4;
    elif (n == 0b1011):
        return i << 12 ^ j << 4 ^ k;
    elif (n == 0b1100):
        return i << 12 ^ j << 8;
    elif (n == 0b1101):
        return i << 12 ^ j << 8 ^ k;
    elif (n == 0b1110):
        return i << 12 ^ j << 8 ^ k << 4;
    elif (n == 0b1111):
        return i << 12 ^ j << 8 ^ k << 4 ^ l;
    else:
        return 0;

def best_round_approximation(U,sbox_form,next_sbox_form):
    """Find the best bias approximation for a round
        input: U - 16-bit round input mask U
               sbox_form: 4-bit current round S-box form
               next_sbox_form: 4-bit next round S-box form
        output: best bias approximation exhausted
    """
    curr_bias = 0
    best_bias = 0
    best_V = 0
    if bit_sum(sbox_form) == 1: # If round has 1 S-box => search for 1
        V = mask(sbox_form,next_sbox_form,0,0,0)
        curr_bias = calculate_approximation(U, V)
        best_bias = curr_bias
        best_V = V
    if bit_sum(sbox_form) == 2: # If round has 2 S-box => search for 2
        for i in possible_output[next_sbox_form]:
            for j in possible_output[next_sbox_form]:
                if i | j == next_sbox_form:
                    V = mask(sbox_form,i,j,0,0)
                    curr_bias = calculate_approximation(U, V)
                    if curr_bias > best_bias:
                        best_bias = curr_bias
                        best_V = V
    if bit_sum(sbox_form) == 3: # If round has 3 S-box => search for 3
        for i in range(1,16):
            for j in range(1,16):
                for k in range(1,16):
                    if i | j | k == next_sbox_form:
                        V = mask(sbox_form,i,j,k,0)
                        curr_bias = calculate_approximation(U, V)
                        if curr_bias > best_bias:
                            best_bias = curr_bias
                            best_V = V
    if bit_sum(sbox_form) == 4: # If round has 4 S-box => search for 4
        for i in range(1,16):
            if i | next_sbox_form == next_sbox_form:
                for j in range(1,16):
                    if j | next_sbox_form == next_sbox_form:
                        for k in range(1,16):                            
                            if k | next_sbox_form == next_sbox_form:
                                for l in range(1,16):
                                    if i | j | k | l == next_sbox_form:
                                        V = mask(sbox_form,i,j,k,l)
                                        curr_bias = calculate_approximation(U, V)
                                        if curr_bias > best_bias:
                                            best_bias = curr_bias
                                            best_V = V
    return best_bias, best_V

def best_approximation(approx):
    """Find the best bias approximation for a S-box position
        input: array of 4 (5 or 6) 4-bit round S-box positions
        output: best approximation + input/output mask to the cipher
    """
    curr_bias = 0
    best_bias = 0
    best_U = 0
    best_V = 0
    masks = []
    for r in range(len(approx)-1): # Loop through all n rounds of the S-box positions
        if r == 0: # Brute force for U and V of the 1st round
            if bit_sum(approx[0]) == 1:
                for i in range(1,16):
                    U = mask(approx[0],i,0,0,0)
                    curr_bias,V = best_round_approximation(U,approx[r],approx[r+1])
                    if curr_bias > best_bias:
                        best_bias = curr_bias
                        best_V = V
                        best_U = U
            if bit_sum(approx[0]) == 2:
                for i in range(1,16):
                    for j in range(1,16):
                        U = mask(approx[0],i,j,0,0)
                        curr_bias,V = best_round_approximation(U,approx[r],approx[r+1])
                        if curr_bias > best_bias:
                            best_bias = curr_bias
                            best_V = V
                            best_U = U
            if bit_sum(approx[0]) == 3:
                for i in range(1,16):
                    for j in range(1,16):
                        for k in range(1,16):
                            U = mask(approx[0],i,j,k,0)
                            curr_bias,V = best_round_approximation(U,approx[r],approx[r+1])
                            if curr_bias > best_bias:
                                best_bias = curr_bias
                                best_V = V
                                best_U = U
            if bit_sum(approx[0]) == 4:
                for i in range(1,16):
                    for j in range(1,16):
                        for k in range(1,16):
                            for l in range(1,16):
                                U = mask(approx[0],i,j,k,l)
                                curr_bias,V = best_round_approximation(U,approx[r],approx[r+1])
                                if curr_bias > best_bias:
                                    best_bias = curr_bias
                                    best_V = V
                                    best_U = U
            masks.append((best_U,best_V))     
            print("Round {}: bestU: {}".format(r+1,bin(best_U)[2:]))
            print("Round {}: bestV: {}".format(r+1,bin(best_V)[2:]))
            print("Round {}: best total bias: {}".format(r+1,best_bias))
        else: # if intermediate rounds
            U = pbox_enc(best_V)
            curr_bias,best_V = best_round_approximation(U,approx[r],approx[r+1])
            best_bias *= 2 * curr_bias
            
            masks.append((U,best_V))   
            print("Round {}: bestU: {}".format(r+1,bin(U)[2:]))
            print("Round {}: bestV: {}".format(r+1,bin(best_V)[2:]))
            print("Round {}: best total bias: {}".format(r+1,curr_bias))
            
    return bin(best_U), bin(pbox_enc(best_V)), best_bias, masks

def print_mask(masks):
    """Print visual representation of S-box positions"""
    text = "----------------------------\n"
    grid = "------------\n"
    for u,v in masks:
        for i in range(12,-1,-4):
            block_u = u>>i & 0b1111
            block_v = v>>i & 0b1111
            if block_u != 0 and block_v != 0:
                text += " {:.3f}|".format(APPROXIMATION[block_u,block_v])
                grid += " x|"
            else:
                text += "      |"
                grid += "  |"
        text += "\n----------------------------\n"
        grid += "\n------------\n"
                
    return text,grid


###############################################################################
#
###########################    Main Program     ###############################
#
###############################################################################

# Enter S-box position here (e.g 0100 0001 0101 0111 == [0b0100,0b0001,0b0101,0b0111])
#approx = [0b0100,0b0001,0b0101,0b0111]
#approx = [0b1001,0b1000,0b1000,0b1010]
approx = [0b1100,0b0010,0b0010,0b1110]

u,v, bias, masks = best_approximation(approx)
print("-----------\nU: {}\nV: {}\nBias: {}".format(u,v,bias))

t,g = print_mask(masks)
print("\n3-round individual S-box approximations")
print(t)
print(g)
