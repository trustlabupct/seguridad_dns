# Atacante — contenedor y scripts
## Ficheros
- `Dockerfile5` -> Construye la imagen del atacante con Python3 y Scapy.
- `poison.py` -> Simulación de ataque de cache poisoning (UDP).
- `poison-doh.py` -> Variante orientada a DoH.
- `tunneling.py` -> Simulación de exfiltración por DNS (UDP).
- `tunneling-dot.py` -> Variante de tunneling sobre DoT.
- `tunneling-doh.py` -> Variante de tunneling sobre DoH.
> Nota: los scripts usan direcciones IP internas fijas (por ejemplo 172.20.0.3 para Unbound y 172.20.0.2 para Knot) y comandos como kdig, curl o scapy. Asegúrate de que la imagen construida (Dockerfile5) incluya las herramientas necesarias (Python3, scapy, kdig/curl) o monta las utilidades desde el contenedor cliente si lo prefieres.

## Construcción de la imagen
En el cmd vas a la ruta donde hayas guardado todos los archivos, por ejemplo en mi caso: `cd C:\Users\User\knot-dns-tfg\atacante`. 
Una vez en la ruta ya ejecutas el siguiente comando:
<pre> docker build -t atacante-debug -f Dockerfile5 . </pre>

## Ejecución del contenedor
Ejecuta el contenedor en la misma red knotnet para que vea a Unbound/Knot/dnsdist:
<pre> docker run -it --rm --network knotnet --name atacante atacante-debug bash </pre>
Dentro del contenedor tendrás los scripts que subiste (ej.: poison.py, poison-doh.py, tunneling*.py).

## Ejecución de scripts — ejemplos
### Cache poisoning (UDP) — poison.py
El script poison.py ataca al resolutor (Unbound) enviando respuestas falsas a 172.20.0.3 . Para ejecutarlo dentro del contenedor atacante:
<pre> python3 poison.py </pre>
**Qué hace**: envía NUM_ATTEMPTS respuestas DNS falsas con rdata="6.6.6.6" hacia la IP 172.20.0.3 intentando inyectar el registro falso.example.test.

### Cache poisoning vía DoH — poison-doh.py
El script poison-doh.py crea paquetes UDP/DNS con fake_ip = "1.2.3.4" y los envía a target_ip = "172.20.0.3" en 200 intentos rápidos:
<pre> python3 poison-doh.py </pre>
**Observación**: este script usa send(pkt) de Scapy y espera 0.005s entre envíos (no es flooding masivo).

### DNS tunneling (dirección directa hacia Knot) — tunneling.py
Envía consultas DNS creadas con Scapy hacia la IP 172.20.0.2 (Knot) para simular túnel/exfiltración.
<pre> python3 tunneling.py </pre>
El script genera subdominios aleatorios (label.example.test) y los consulta num_queries veces.

### Tunneling usando DoT — tunneling-dot.py
Usa kdig con +tls para enviar consultas por DoT hacia @172.20.0.3:
<pre> python3 tunneling-dot.py </pre>
Fijarse que el script ejecuta internamente kdig y espera intervalos entre consultas.

### Tunneling usando DoH — tunneling-doh.py
Genera consultas DNS binarias usando kdig y las envía por DoH con curl a `https://172.20.0.4/dns-query`:
<pre> python3 tunneling-doh.py </pre>
Asegúrate de que la URL `https://172.20.0.4/dns-query` es la que corresponde a tu contenedor dnsdist en la red knotnet (la IP puede variar según cómo crees la red/contenedores).

## Consejos prácticos
- Los scripts usan IP internas fijas: 172.20.0.2 (Knot) y 172.20.0.3 (Unbound). Si al arrancar tus contenedores esas IP cambian, edita los scripts antes de ejecutarlos para poner las IP correctas, o bien asigna la misma subred/IP al crear la red Docker (--subnet=172.20.0.0/16) para que coincidan. Los scripts están escritos con esas IPs como constantes.
- Algunos scripts (DoT/DoH) invocan kdig, curl o requieren scapy. Verifica que Dockerfile5 incluya scapy y que la imagen o el contenedor cliente tenga kdig y curl. Si no, añade esos paquetes al Dockerfile o ejecuta los scripts desde el contenedor cliente donde ya tengas esas herramientas.
