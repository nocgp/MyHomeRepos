# For Ubuntu only

#!/bin/bash

# Install SOLR

addgroup jetty
useradd -g jetty -d /home/jetty jetty
cd /opt
wget https://archive.apache.org/dist/lucene/solr/4.9.0/solr-4.9.0.tgz
wget http://ftp.fau.de/eclipse/jetty/stable-9/dist/jetty-distribution-9.2.1.v20140609.tar.gz
tar xzf /opt/jetty-distribution-9.2.1.v20140609.tar.gz  -C /opt/; mv /opt/jetty-distribution-9.2.1.v20140609 /opt/jetty-9.2.1
tar xzf /opt/solr-4.9.0.tgz -C /opt/; mv /opt/solr-4.9.0/example/* /opt/solr-4.9.0/;
cp /opt/solr-4.9.0/webapps/solr.war /opt/jetty-9.2.1/webapps/; cp -r /opt/solr-4.9.0/lib/ext/* /opt/jetty-9.2.1/lib/ext/; cp -r /opt/solr-4.9.0/solr/collection1 /opt/solr-4.9.0/; cp -r /opt/solr-4.9.0/example-schemaless/solr/collection1/* /opt/solr-4.9.0/collection1/
cp /mnt/software/solr/jetty /etc/default/jetty
cp /mnt/software/solr/http.ini /opt/jetty-9.2.1/start.d/http.ini
cp /mnt/software/solr/solrconfig.xml /opt/solr-4.9.0/collection1/conf/solrconfig.xml
cp /mnt/software/solr/schema.xml /opt/solr-4.9.0/collection1/conf/schema.xml
cp /mnt/software/solr/logging.properties dest=/opt/jetty-9.2.1/etc/logging.properties owner=jetty
ln -s /opt/jetty-9.2.1/bin/jetty.sh /etc/init.d/jetty
mkdir /var/log/jetty-9.2.1; chown -R jetty:jetty /opt/solr-4.9.0/; chown -R jetty:jetty /var/log/jetty-9.2.1/; chown -R jetty:jetty /opt/jetty-9.2.1
update-rc.d jetty defaults

# Configure jetty loggin
mkdir /opt/jetty-9.2.1/lib/logging
cp /opt/jetty-9.2.1/lib/ext/log4j-1.2.17.jar /opt/jetty-9.2.1/lib/logging/
cp /opt/jetty-9.2.1/lib/ext/slf4j-log4j12-1.7.6.jar /opt/jetty-9.2.1/lib/logging/
cp /opt/jetty-9.2.1/lib/ext/slf4j-api-1.7.6.jar /opt/jetty-9.2.1/lib/logging/
chown -R jetty:jetty /opt/jetty-9.2.1/lib/logging/

echo "--exec
-Dsolr.solr.home=/opt/solr-4.9.0 

--module=websocket,resources,ext,jsp,logging" >> /opt/jetty-9.2.1/start.ini

sed -i.bak '49s/.*JETTY_HOME/JETTY_HOME\=\/opt\/jetty-9.2.1\//g' /etc/init.d/jetty

sudo -u jetty /etc/init.d/jetty start

