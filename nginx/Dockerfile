FROM nginx:alpine

RUN apk add --no-cache openssl
RUN mkdir -p /etc/nginx/ssl

# Gerar certificado SSL
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/localhost.key \
    -out /etc/nginx/ssl/localhost.crt \
    -subj "/C=BR/ST=SP/L=SP/O=Dev/CN=localhost"

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]