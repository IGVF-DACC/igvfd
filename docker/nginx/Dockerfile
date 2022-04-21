FROM nginx:1.21.4

RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY ./config/nginx/production.conf /etc/nginx/nginx.conf
