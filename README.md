There are two hosts in my private network:

- registry: chupakabra.tk:55022
- containers: chupakabra.tk:56022

SSH:

- user: barackobama
- password: passwd!@#
- group: wheel
    
You are able to reboot, shutdown, change any params.

---------------------------------------------------------------------------------
Demo App you can see via: http://devopstz.chupakabra.tk/

It's proxing by Nginx to "containers" host.
Also you can pull it by DSTNAT: http://chupakabra.tk:10000/

Demo app deploys to container host from "registry" host's docker-registry daemon.
It was installed from CentOs repo.

Demo app written by me on Flask and uses Cassandra as DB via official
Cassandra 2.1 docker image.
It's config file "config.json' mapped from /opt/devopstz/demoapp/config.json

You can buil it on your machine:
```
cd devopstz/demoapp/ && docker build -t demoapp .
```
and push it to docker registry (available by chupakabra.tk:15000):
```
docker tag demoapp:latest 172.22.22.201:5000/demoapp:1.0
docker push 172.22.22.201:5000/demoapp:1.0
```
---------------------------------------------------------------------------------
Cassandra DB data stored on mapped dir: /opt/devopstz/cassandra.
You can run on "containers" host:
```
/opt/apache-cassandra-3.0.8/bin/cqlsh --cqlversion=3.2.1 localhost
```
and create schema:
```
CREATE KEYSPACE fake_data WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };
create table fake_data.users (username varchar PRIMARY KEY, email varchar, name varchar, ipaddr inet);
```
---------------------------------------------------------------------------------
I wrote two versions of systemd.service:
- stop/start containers;
- stop containers; remove images; pull new images; start containers (use now).

P. S. I tried made it all on CoreOs, but i stacked on libvirt bug and drop it now.
      Also i spent time to other things, like Nginx proxy to docker registry,
      but some of that was not success for me according to time deficit.
