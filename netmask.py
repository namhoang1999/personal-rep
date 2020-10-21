# 128. 96. 34. 15
# 255.255.255.128
# 128. 96. 34.  0


def cidr_to_netmask(cidr):
    h = int(cidr/8)
    t = 0
    for i in range(cidr%8):
        t += 2**(8-1-i)
    mask = [255 for _ in range(h)]
    mask.append(t)
    return tuple(mask),'.'.join(map(str,mask))

def str_to_ip(s):
    s = s.replace(' ','')
    ip = tuple(map(int,s.split('.')))
    return ip,s
    
s = input('Input IP address with netmask').split('/')
ip = s[0]
cidr = int(s[1])

ip,ip_str = str_to_ip(ip)
mask,mask_str = cidr_to_netmask(cidr)
subnet = tuple(map(lambda x : x[0] & x[1],zip(ip,mask)))

print('IP address:', ip_str)
print('Netmask:', mask_str)

print('Subnet','.'.join(map(str,mask)))