FROM centos:7

RUN yum -y install httpd wget unzip ; yum clean all ; systemctl enable httpd
RUN wget https://jih123.s3.ap-northeast-2.amazonaws.com/index.zip
RUN unzip index.zip -d /var/www/html ; rm -rf index.zip

EXPOSE 80
ENTRYPOINT ["/usr/sbin/httpd", "-D", "FOREGROUND"]
