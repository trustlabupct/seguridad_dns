# dnsdist — resolutor DoH
## Ficheros
- `Dockerfile4` -> Construye la imagen de dnsdist.
- `dnsdist.conf` -> Configuración: escucha en 443 (DoH) y 853 (DoT), certificados TLS y reenvío hacia Unbound.
- `cert.pem`, `key.pem` -> Certificados TLS para DoH/DoT (son los mismos que en unbound).

## Construcción de la imagen
En el cmd vas a la ruta donde hayas guardado todos los archivos, por ejemplo en mi caso: `cd C:\Users\User\knot-dns-tfg\doh-resolutor`. 
Una vez en la ruta ya ejecutas el siguiente comando:
<pre> docker build -t dnsdist-doh -f Dockerfile4 . </pre>

## Ejecución del contenedor
> Usa la misma red que el resto (knotnet) y mapea el 443 del contenedor al 8443 del host
<pre> docker run -d --name doh-resolutor --network knotnet ^
 -p 8443:443 ^
 -v "%cd%:/etc/dnsdist" ^
 dnsdist-doh
</pre>
- El volumen monta esta carpeta (donde están `dnsdist.conf`, `cert.pem`, `key.pem`) en /etc/dnsdist — es lo que espera tu dnsdist.conf.
- Asegúrate de que Unbound está accesible en la red `knotnet` con IP `172.20.0.3` (o cambia esa IP en `dnsdist.conf` si usas otra).

## Comprobación rápida
- El contenedor debe exponer DoH en `https://localhost:8443/dns-query`.
- Si no resuelve, revisa:
    - Que Unbound está arriba y accesible en `172.20.0.3`.
    - Que los archivos `cert.pem` y `key.pem` se están montando correctamente en `/etc/dnsdist`.
