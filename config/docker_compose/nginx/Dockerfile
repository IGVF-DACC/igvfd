FROM nginx:1.21.4

RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY ./config/docker_compose/nginx/nginx.conf /etc/nginx
