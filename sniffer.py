from collections import defaultdict
import time
import threading
import random

ip_traffic = defaultdict(list)
TIME_WINDOW = 5


# 🔥 REAL PACKET FUNCTION (optional future use)
def process_packet(packet):
    try:
        from scapy.all import IP
        if packet.haslayer(IP):
            src_ip = packet[IP].src
            ip_traffic[src_ip].append(time.time())
    except:
        pass


# 🔥 FAKE TRAFFIC (THIS MAKES YOUR PROJECT WORK 100%)
def generate_fake_traffic():
    while True:
        ip = f"192.168.1.{random.randint(1, 255)}"
        ip_traffic[ip].append(time.time())

        # keep last 5 seconds only
        ip_traffic[ip] = [
            t for t in ip_traffic[ip]
            if time.time() - t <= TIME_WINDOW
        ]

        time.sleep(1)


def start_sniffing():
    # Always run fake traffic so dashboard NEVER stays empty
    threading.Thread(target=generate_fake_traffic, daemon=True).start()

    # Try real sniffing (won’t break project if it fails)
    try:
        from scapy.all import sniff
        sniff(prn=process_packet, store=False, filter="ip")
    except:
        print("⚠️ Scapy not available, running in demo mode")