FROM nginx:perl

RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/production/nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
