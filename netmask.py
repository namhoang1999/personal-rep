# TODO: Convert addresses from tuples to binary
"""
def cidr_to_netmask(cidr):
    t = sum(2**(8-1-i) for i in range(cidr%8))
    mask = [255 if i < int(cidr/8) else t if i == int(cidr/8) else 0 for i in range(4)]
    return tuple(mask)

def f(cidr):
    return bin(int('1'*cidr + '0'*(32-cidr),2))

def ip_to_str(ip):
    ip = str(ip)[2:]
    return '.'.join([int(ip[x:x+8],2) for x in range(0,32,8)])
    
def str_to_ip(st):
    st = (st.replace(' ','')).split('.')
    return bin(int(''.join(st),2))

"""

def print_a(t):
    return '.'.join(map(str,t))

def cidr_to_netmask(cidr):
    t = sum(2**(8-1-i) for i in range(cidr%8))
    mask = [255 if i < int(cidr/8) else t if i == int(cidr/8) else 0 for i in range(4)]
    return tuple(mask)

def str_to_ip(s):
    s = s.replace(' ','')
    ip = tuple(map(int,s.split('.')))
    return ip

# since using ~ will return a signed number (eg. ~255 = -256)
# this method returns a number's unsigned binary complement 
def unsigned_not(n):    
    mask = 0b11111111
    return int(~n&mask)
    
#s = input('Input IP address with netmask').split('/')
s = '202.10.133.11/24'.split('/')
ip_input   = s[0]
cidr_input = int(s[1])

ip          = str_to_ip(ip_input)
netmask     = cidr_to_netmask(cidr_input)
network_id  = tuple(map(lambda x : x[0] & x[1],zip(ip,netmask)))

# Take the complement of netmask
bw_not_netmask = tuple(map(unsigned_not,netmask))
# Bit-wise OR it with the IP address to obtain broadcast address
broadcast = tuple(map(lambda x: x[0] | x[1], zip(bw_not_netmask, ip)))

print('IP address: ', ip_input)
print('Netmask:    ', print_a(netmask))
print('Network ID: ', print_a(network_id))
print('Broadcast:  ', print_a(broadcast))
print('Total hosts:', 2**(32-cidr_input)-2)