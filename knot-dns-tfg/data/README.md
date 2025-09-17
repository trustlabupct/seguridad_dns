# Knot DNS (autoritativo + DNSSEC)
## Ficheros
Coloca en data/ los archivos de configuración de Knot:
- `knot.conf` -> Configuración principal del servidor autoritativo.
- `example.zone` -> Archivo de zona con registros de ejemplo (example.test).
- `Dockerfile` -> Construye la imagen de Knot.
- `keys/` -> Carpeta para las claves DNSSEC (KSK/ZSK).

## Construcción de la imagen
En el cmd vas a la ruta donde hayas guardado todos los archivos, por ejemplo en mi caso: `cd C:\Users\User\knot-dns-tfg`. 
Una vez en la ruta ya ejecutas el siguiente comando:
<pre> docker build -t knot-server . </pre>
## Ejecución del contenedor
<pre> docker run -d --name knot --network knotnet -p 5300:53/udp -p 5300:53/tcp -v "%cd%/data:/etc/knot" knot-server </pre>
> (Se usa la red knotnet y se monta la carpeta data en /etc/knot)
## Generación de claves dentro del contenedor
<pre>
  docker exec -it knot /bin/bash
  keymgr example.test. generate algorithm=RSASHA256 size=2048 ksk=true > /etc/knot/keys/ksk.key
  keymgr example.test. generate algorithm=RSASHA256 size=2048 zsk=true > /etc/knot/keys/zsk.key
</pre>
## Verificación
- Estado de la zona desde knot:
<pre> knotc zone-status example.test </pre>
- Consultas firmadas (desde el cliente):
<pre> dig @unbound example.test +dnssec +multi </pre>
## Captura en knot para pruebas
<pre>docker exec -it knot sh
apt update && apt install -y tcpdump
</pre>
> (Por si se quiere comprobar alguna cosa)
