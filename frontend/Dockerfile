FROM node:18-slim AS build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

FROM nginx:alpine AS prod

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

ENV PORT 8080
EXPOSE 8080


CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
# CMD ["npm", "run", "dev-exposed"]