import sys
from optparse import OptionParser
from datetime import datetime
import time
import dns.name
import dns.message
import dns.query
import dns.flags
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
    target_address = "example.com" + str(iter)
    previous_serial = get_serial(target_address, server_root)

    
    while 1:
        iter += 1
        target_address = "example.com" + str(iter)
        current_serial = get_serial(target_address, server_root)
        # potential bug, if neg 1 run again until its not for previous
        
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
        
        # add if when we get down to the wire
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "test"])
        subprocess.run(["git", "push"])


def main(argv):
    # hit the other addresses
    roots = [("feb_1_verisign(a)", "198.41.0.4"),
    ("feb_1_USC", "199.9.14.201"),
    ("feb_1_CogentCom", "192.33.4.12"),
    ("feb_1_UM", "199.7.91.13"),
    ("feb_1_NASA", "192.203.230.10"),
    ("feb_1_ISC", "192.5.5.241"),
    ("feb_1_US DD (NIC)", "192.112.36.4"),
    ("feb_1_Army", "198.97.190.53"),
    ("feb_1_Netnod", "192.36.148.17"),
    ("feb_1_verisign (j)", "192.58.128.30"),
    ("feb_1_RIPE", "193.0.14.129"),
    ("feb_1_ICANN", "199.7.83.42"),
    ("feb_1_WIDE", "202.12.27.33")]


    for r in roots:
        x = threading.Thread(target=start_recording, args=(r[0], r[1]))
        x.start()


if __name__ == "__main__":
    main(sys.argv[1:])

    # root changes seem to consistently be between 22:00 and 23:00, as well as between 10:00 and 11:00 (MST)




# import git
# import time
# import subprocess


# iter = 0
# while 1:
#     iter += 1

#     with open("test.txt", 'a') as the_file:
#         first = str(iter) + "\n"
#         the_file.write(first)

#     # repo = git.Repo('/Nlarseny/git_test')
#     # repo.git.add('--all')  # to add all the working files.
#     # repo.git.commit('-m', 'commit message from python script', author='test_user@test.com')
#     # origin = repo.remote(name='origin')
#     # origin.push()

#     subprocess.run(["git", "add", "."])
#     subprocess.run(["git", "commit", "-m", "test"])
#     subprocess.run(["git", "push"])


#     time.sleep(5)
