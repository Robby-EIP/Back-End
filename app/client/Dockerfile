FROM node:14.18.2-alpine

WORKDIR /app/client

COPY package*.json ./

RUN npm install -g @angular/cli @angular-devkit/build-angular
RUN npm install

EXPOSE 4200

CMD ["npm", "start"]