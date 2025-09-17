FROM debian:bookworm

# Instalar herramientas necesarias
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    wget \
    gnupg \
    curl \
    knot

# Añadir la clave GPG del repositorio oficial de CZ.NIC
RUN wget -O /usr/share/keyrings/cznic-labs-pkg.gpg https://pkg.labs.nic.cz/gpg

# Añadir el repositorio de Knot DNS para Debian 12 (Bookworm)
RUN echo "deb [signed-by=/usr/share/keyrings/cznic-labs-pkg.gpg] https://pkg.labs.nic.cz/knot-dns bookworm main" > /etc/apt/sources.list.d/knot.list

# Actualizar e instalar Knot DNS
RUN apt-get update && apt-get install -y knot

# Crear carpetas necesarias
RUN mkdir -p /etc/knot /zones /run/knot

# Copiar archivos de configuración y zona
COPY data/knot.conf /etc/knot/knot.conf
COPY data/example.zone /zones/example.zone

# Exponer puertos DNS (por buenas prácticas aunque se puede mapear luego)
EXPOSE 53/udp
EXPOSE 53/tcp

# Comando de arranque
CMD [ "knotd", "-c", "/etc/knot/knot.conf"]

