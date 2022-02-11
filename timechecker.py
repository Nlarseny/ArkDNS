import sys
from optparse import OptionParser
from datetime import datetime
import time
import dns.name
import dns.message
import dns.query
import dns.flags
import dns
import threading
import subprocess

def get_serial(target, server_root):
    #domain = '199.7.91.13' aka the target
    #name_server = '8.8.8.8' aka server_root # @ part of dig
    ADDITIONAL_RDCLASS = 65535

    domain = dns.name.from_text(target)
    if not domain.is_absolute():
        domain = domain.concatenate(dns.name.root)

    request = dns.message.make_query(domain, dns.rdatatype.A, use_edns=0) # use_edns = 0? for below code

    try:
        response = dns.query.udp(request, server_root, timeout=2.0) # timeout 2 seconds, throws timeout exception (try around it), .4

        for rrset in response.authority:
            if rrset.rdtype == dns.rdatatype.SOA and rrset.name == dns.name.root: # makes sure its the root that owns the record
                return int(rrset[0].serial)
            else:
                print("error explanation")
    except Exception as e:
        print("[Domain Analyzer][Error] %s" % e)
        return -1


def start_recording(root_name, server_root):
    file_name = str(root_name) + ".txt"
    # with open(file_name, 'a') as the_file:
	#    first = file_name
	 #   the_file.write(first)

    iter = 0
    target_address = "example.com_byuimaallab" + str(iter)
    previous_serial = get_serial(target_address, server_root)

    
    while 1:
        iter += 1
        target_address = "example.com_byuimaallab" + str(iter)
        current_serial = get_serial(target_address, server_root)
        
        if current_serial != previous_serial or current_serial == -1:
            print(iter)
            if current_serial == -1:
                with open(file_name, 'a') as the_file:
                    first = str(datetime.now().time()) + " TIMED OUT" + "\n"
                    the_file.write(first)
            else:
                print(file_name)
                with open(file_name, 'a') as the_file:
                        first = str(datetime.now().time()) + " " + str(current_serial) + "\n"
                        the_file.write(first)
            if current_serial != -1:
                previous_serial = current_serial
        
        time.sleep(600)
        

        with open("nohup.out", 'w') as the_file:
            first = str(iter)
            the_file.write(first)



def main(argv):
    # hit the other addresses
    roots = [("verisign(a)", "198.41.0.4"),
    ("USC", "199.9.14.201"),
    ("CogentCom", "192.33.4.12"),
    ("UM", "199.7.91.13"),
    ("NASA", "192.203.230.10"),
    ("ISC", "192.5.5.241"),
    ("US_DD(NIC)", "192.112.36.4"),
    ("Army", "198.97.190.53"),
    ("Netnod", "192.36.148.17"),
    ("verisign(j)", "192.58.128.30"),
    ("RIPE", "193.0.14.129"),
    ("ICANN", "199.7.83.42"),
    ("WIDE", "202.12.27.33")]


    for r in roots:
        x = threading.Thread(target=start_recording, args=(r[0], r[1]))
        x.start()


if __name__ == "__main__":
    main(sys.argv[1:])



# roots = [("verisign(a)", "198.41.0.4"),
#     ("USC", "199.9.14.201"),
#     ("CogentCom", "192.33.4.12"),
#     ("UM", "199.7.91.13"),
#     ("NASA", "192.203.230.10"),
#     ("ISC", "192.5.5.241"),
#     ("US_DD(NIC)", "192.112.36.4"),
#     ("Army", "198.97.190.53"),
#     ("Netnod", "192.36.148.17"),
#     ("verisign(j)", "192.58.128.30"),
#     ("RIPE", "193.0.14.129"),
#     ("ICANN", "199.7.83.42"),
#     ("WIDE", "202.12.27.33"),
#     ("verisign(a)_v6", "2001:503:ba3e::2:30"), # adding the ipv6's
#     ("USC_v6", "2001:500:200::b"),
#     ("CogentCom_v6", "2001:500:2::c"),
#     ("UM_v6", "2001:500:2d::d"),
#     ("NASA_v6", "2001:500:a8::e"),
#     ("ISC_v6", "2001:500:2f::f"),
#     ("US_DD(NIC)_v6", "2001:500:12::d0d"),
#     ("Army_v6", "2001:500:1::53"),
#     ("Netnod_v6", "2001:7fe::53"),
#     ("verisign(j)_v6", "2001:503:c27::2:30"),
#     ("RIPE_v6", "2001:7fd::1"),
#     ("ICANN_v6", "2001:500:9f::42"),
#     ("WIDE_v6", "2001:dc3::35")]
