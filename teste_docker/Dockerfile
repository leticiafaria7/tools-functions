FROM node:14
WORKDIR G:\Meu Drive\5. Cursos\programming\tools-functions\teste_docker\app-node
ARG PORT=6000
ENV PORT=$PORT
EXPOSE $PORT
COPY . .
RUN npm install
ENTRYPOINT npm start