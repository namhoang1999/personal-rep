# Convert IP int to str
def ip_to_str(ip):
    o1 = int(ip / 256**3) % 256
    o2 = int(ip / 256**2) % 256
    o3 = int(ip / 256) % 256
    o4 = int(ip) % 256
    return '{}.{}.{}.{}'.format(o1,o2,o3,o4)

# Convert str to IP int
def str_to_ip(st):
    o = list(map(int, st.split('.')))
    c = ''
    if o[0] <= 127:
        c = 'A'
    elif o[0] <= 191:
        c = 'B'
    elif o[0] <= 223:
        c = 'C'
    else:
        c = 'Unidentified'
        
    return (256**3 * o[0]) + (256**2 * o[1]) + (256 * o[2]) + o[3],t
    
# Convert CIDR notation to netmask
def cidr_to_netmask(cidr):
    return int('1'*cidr + '0'*(32-cidr),2)

# since using ~ will return a signed number (eg. ~255 = -256)
# this method returns a number's unsigned binary complement 
def unsigned_not(n):    
    mask = 0b11111111
    return int(~n&mask)

if __name__ == '__main__':    
    #s = input('Input IP address with netmask (eg. 202.10.133.19/20').split('/')
    s = '202.10.133.19/20'.split('/')
    ip,t   = str_to_ip(s[0])
    cidr = int(s[1])
    netmask     = cidr_to_netmask(cidr)
    network_id  = ip & netmask
    
    # Calculate the wildcard of network (netmask compliment)
    wildcard = unsigned_not(netmask)
    # Bit-wise OR it with the IP address to obtain broadcast address
    broadcast = wildcard | ip

    total_host = 2**(32-cidr)
    usable_host = total_host - 2
    ip_min = network_id - network_id % 256 + 1
    ip_max = ip_min + usable_host - 1
    
    print(f'IP address: {ip_to_str(ip)}')
    print(f'Netmask:    {ip_to_str(netmask)}')
    print(f'Wildcard:   {ip_to_str(wildcard)} \n')

    print(f'Total hosts:       {total_host}')      # 1 address for broadcast, 1 for host address
    print(f'Total usable host: {2**(32-cidr)-2}')    
    print(f'Network ID: {ip_to_str(network_id)}/{cidr} (Class {t})')
    print(f'IP min:     {ip_to_str(ip_min)}')
    print(f'IP max:     {ip_to_str(ip_max)}')
    print(f'Broadcast:  {ip_to_str(broadcast)}')
