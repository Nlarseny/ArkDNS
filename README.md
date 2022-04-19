This repository is used on CAIDA Ark nodes.

Each node has its own folder (i.e. beg-rs, san-us, etc.)

The program run on each node is tophour.py, to run on node cd in the correct folder (matches with the node you are sshed into) and then use the following command: nohup python3 ../tophour.py & (or /usr/local/ark/bin/python3 ../tophour.py & if python3 is not liking the dnspython package you tried to pip install in)

The timeout_counter.py program simply 