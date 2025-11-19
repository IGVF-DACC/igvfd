FROM public.ecr.aws/nginx/nginx:1.29.3

RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY ./config/nginx/production.conf /etc/nginx/nginx.conf
