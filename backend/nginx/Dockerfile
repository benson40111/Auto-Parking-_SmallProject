FROM nginx:alpine
RUN rm /etc/nginx/conf.d/*
COPY proxy.conf /etc/nginx/conf.d/
COPY cloudflare-allow.conf /etc/nginx/
