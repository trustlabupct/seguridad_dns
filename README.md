# Seguridad_dns
## Resumen
Repositorio autocontenido para reproducir el entorno sobre seguridad en DNS. Incluye todos los ficheros de los servicios (Knot autoritativo con DNSSEC, Unbound resolutor validante con DoT, dnsdist para DoH, contenedor cliente y contenedor atacante con scripts).
Sigue las instrucciones siguientes tal cual para levantar el entorno en una máquina con Docker.

## Requisitos previos
- Docker instalado (recomendado versión moderna).
- No es necesario tener herramientas dig, curl, openssl en el host: el contenedor cliente las incluye.

## 1 - Crear la red Docker (IMPORTANTE para IPs fijas)
En este proyecto los ficheros de configuración usan IPs internas. Para que los scripts y confs funcionen tal cual, crea la red con la misma subred:
<pre> docker network create --driver bridge --subnet=172.20.0.0/16 knotnet </pre>
Si prefieres no usar IPs fijas (y editar las confs para usar nombres de servicio), puedes crear la red sin --subnet:
<pre> docker network create knotnet </pre>

## 2 — Orden de arranque (obligatorio)
Levanta los contenedores en este orden para que cada servicio obtenga las IPs/rutas esperadas por las confs y los scripts:
1. Knot (autoritativo + DNSSEC)
2. Unbound (resolutor validante + DoT)
3. dnsdist (proxy DoH)
4. Cliente (shell con dig/kdig/curl)
5. Atacante (scripts Python/Scapy)

## 3 — Comandos exactos para construir y arrancar
Los comandos concretos están documentados dentro de cada carpeta en su correspondiente README:

## 4 - Problemas habituales y soluciones rápidas
- No responde DoH/DoT: comprueba que cert.pem y key.pem están montados y que los paths en dnsdist.conf / unbound.conf coinciden.
- Unbound no valida (SERVFAIL / no AD): revisa root.key (ancla) y root.hints; confirma que auto-trust-anchor-file apunta al archivo correcto.
- dnsdist no reenvía: revisa IP configurada en dnsdist.conf y que unbound esté en la misma red.
- Scripts atacante sin alcance: comprobar IPs internas o crear la red con la subred indicada para que coincidan las IPs fijas.
