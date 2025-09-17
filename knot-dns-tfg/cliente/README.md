# Cliente (contenedor de pruebas)
## Ficheros
- `Dockerfile3` (incluye herramientas como dig, curl, etc. para validar).

## Construcción de la imagen
En el cmd vas a la ruta donde hayas guardado todos los archivos, por ejemplo en mi caso: `cd C:\Users\User\knot-dns-tfg\cliente`. 
Una vez en la ruta ya ejecutas el siguiente comando:
<pre> docker build -t cliente-dig -f Dockerfile3 . </pre>

## Ejecución del contenedor
<pre> docker run -it --rm --network knotnet --name cliente cliente-dig bash </pre>
> Entra en una shell interactiva conectada a la red knotnet.

## Comandos de validación (dentro del contenedor)
- DNSSEC vía Unbound:
<pre> dig @unbound example.test +dnssec +multi </pre>
- Consulta directa al autoritativo (si lo necesitas):
<pre> dig @knot example.test SOA +multi </pre>
- Probar DoH (si has levantado dnsdist en :443 y mapeado a 8443):
    1) Desde el contenedor cliente se creó un archivo que contenía una consulta DNS válida 
       para example.test (tipo A). Para ello, se ejecutó el siguiente comando: 
        <pre> echo -n -e '\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x04test\x00\00\x01\x00\x01' > query.bin </pre>
    > Este archivo (query.bin) contiene una consulta DNS en formato binario tal como la espera un servidor compatible con DoH. 
    2) A continuación, se utilizó curl para enviar la consulta como una petición HTTPS con el tipo de contenido adecuado: 
        <pre> curl -k -H 'Content-Type: application/dns-message' \ --data-binary @query.bin \ https://doh-resolutor:443/dns-query --output - </pre>

Para salir del contenedor: `exit`.
