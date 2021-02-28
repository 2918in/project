FROM centos/httpd

RUN yum -y install wget unzip
RUN wget https://jih123.s3.ap-northeast-2.amazonaws.com/index.zip
RUN unzip index.zip -d /var/www/html ; rm -rf index.zip

