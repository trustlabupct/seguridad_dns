import random
import string
import time
import subprocess

# Configuración
doh_url = "https://172.20.0.4/dns-query"  # URL de tu servidor DoH
domain = "example.test"
num_queries = 20
interval = 0.5
label_length = 12
unbound_ip = "172.20.0.3"

def random_label(length):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def send_doh_query():
    label = random_label(label_length)
    full_domain = f"{label}.{domain}"
    print(f"Sending DoH query for {full_domain}")
    
    # Construir binario DNS con kdig
    kdig_cmd = [
        "kdig", "+dnssec", full_domain,
        f"@{unbound_ip}", "-p", "53",
        "+noall", "+qr", "-d"
    ]

    # Ejecutar kdig y redirigir salida binaria a query.bin
    with open("query.bin", "wb") as f:
        subprocess.run(kdig_cmd, stdout=f)

    # Enviar la petición DoH
    curl_cmd = [
    "curl", "-s", "-k",
    "--http2-prior-knowledge",
    "-H", "Content-Type: application/dns-message",
    "--data-binary", "@query.bin",
    doh_url
    ]
    subprocess.run(curl_cmd)

# Enviar múltiples consultas
for _ in range(num_queries):
    send_doh_query()
    time.sleep(interval)
