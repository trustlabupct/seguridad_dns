import subprocess
import random
import string
import time

# Configuración
unbound_ip = "172.20.0.3"        # IP de tu resolutor Unbound
domain = "example.test"          # Dominio bajo tu control
num_queries = 20                 # Número de consultas a enviar
interval = 0.5                   # Intervalo entre consultas
label_length = 12                # Longitud del subdominio

def random_label(length):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def send_dns_query_dot():
    label = random_label(label_length)
    full_domain = f"{label}.{domain}"
    print(f"Sending DoT query for {full_domain}")
    
    subprocess.run([
        "kdig", "+tls", f"@{unbound_ip}", full_domain
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Enviar múltiples consultas
for _ in range(num_queries):
    send_dns_query_dot()
    time.sleep(interval)
