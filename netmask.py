# 128. 96. 34. 15
# 255.255.255.128
# 128. 96. 34.  0

def print_a(t):
    return '.'.join(map(str,network_id))

def cidr_to_netmask(cidr):
    t = sum(2**(8-1-i) for i in range(cidr%8))
    mask = [255 if i < int(cidr/8) else t if i == int(cidr/8) else 0 for i in range(4)]
    return tuple(mask)

def str_to_ip(s):
    s = s.replace(' ','')
    ip = tuple(map(int,s.split('.')))
    return ip
    
#s = input('Input IP address with netmask').split('/')
s = '196.168.45.55/21'.split('/')
ip_input = s[0]
cidr_input = int(s[1])

ip          = str_to_ip(ip_input)
netmask     = cidr_to_netmask(cidr_input)
print(ip)
print(netmask)
print(tuple(zip(ip,netmask)))
network_id  = tuple(map(lambda x : x[0] & x[1],zip(ip,netmask)))
address     = (ip[0],ip[1],ip[2],ip[3]-1)

print('IP address:', print_a(ip))
print('Netmask:', print_a(netmask))
print('Address', print_a(address))

print('Network ID',print_a(network_id))