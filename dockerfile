FROM node:latest
WORKDIR /usr/src/app
COPY package.json package-lock.json* ./

# Instala las dependencias
RUN npm install --production

# Copia el resto del código fuente
COPY . .

# Expone el puerto de la app
EXPOSE 8081

# Comando para iniciar la app (ajusta si usas otro script)
CMD ["npm", "start"]
