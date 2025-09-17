# Unbound (resolutor + DoT)
## Ficheros
- `unbound.conf` -> Configuración del resolutor: validación DNSSEC, DoT (TLS), forwarding y stub hacia Knot.
- `Dockerfile2` -> Construye la imagen de Unbound.
- `root.hints` -> Lista de servidores raíz.
- `root.key` -> Ancla de confianza para validación DNSSEC.
- `cert.pem`, `key.pem` -> Certificados TLS autofirmados para habilitar DoT.

## Construcción de la imagen
En el cmd vas a la ruta donde hayas guardado todos los archivos, por ejemplo en mi caso: `cd C:\Users\User\knot-dns-tfg\unbound`. 
Una vez en la ruta ya ejecutas el siguiente comando:
<pre> docker build -t unbound-debug -f Dockerfile2 . </pre>
## Ejecución del contenedor
<pre> docker run -d --name unbound --network knotnet ^
 -v "%cd%:/etc/unbound" ^
 -p 5301:53/udp -p 5301:53/tcp ^
 -p 853:853 ^
 unbound-debug
 </pre>

## Archivos clave en la configuración
- `unbound.conf` (interfaz 0.0.0.0, puerto 53 y 853 con TLS, validación DNSSEC con root.key, forwarding a 1.1.1.1 y 8.8.8.8, stub-zone hacia Knot en 172.20.0.2).
- `root.key` (ancla de confianza para DNSSEC).
- `root.hints` (servidores raíz).
- `cert.pem` y `key.pem` (certificados TLS para el servicio DoT).
## Validación básica
- Desde un contenedor cliente:
<pre> dig @unbound example.test +dnssec +multi </pre>
## Generación de certificados autofirmados 
Los certificados se generaron usando openssl desde un contenedor auxiliar Alpine, usando el comando: 
<pre>
docker run --rm -v "%cd%:/work" -w /work alpine sh -c ^ 
"apk add openssl && openssl req -x509 -nodes -days 365 -newkey rsa:2048 ^ -keyout key.pem -out cert.pem -subj '/CN=unbound' ^ -addext 'subjectAltName=DNS:unbound,DNS:localhost'" 
</pre>
> Los archivos generados se copiaron al contenedor a través del Dockerfile. 
