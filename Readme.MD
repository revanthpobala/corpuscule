#CORPUSCULE

This project uses  [Bigchaindb](https://github.com/bigchaindb/bigchaindb) as a backend database.

## Dependencies
* Rethink DB / MongoDB 
* Docker
* BigchainDB

## Docker Images

For Mac installation, follow the following commands

**Pull the images from Docker**

**BigchainDB:** `docker pull bigchaindb/bigchaindb:master`

**RethinkDB:** `docker pull rethinkdb:2.3`

#####Create Bigchain configuration file on Mac

`docker run 
  --rm 
  --volume $HOME/bigchaindb_docker:/data 
  bigchaindb/bigchaindb:master 
  -y configure 
  rethinkdb`
  
#####Run the RethinkDB server on Docker

`docker run 
  --name=rethinkdb 
  --publish=28015:28015 
  --publish=8080:8080 
  --restart=always 
  --volume $HOME/bigchaindb_docker:/data 
  rethinkdb:2.3`
  
#####Run BigchainDB on Mac

`docker run 
  --name=bigchaindb 
  --publish=9984:9984 
  --restart=always 
  --volume=$HOME/bigchaindb_docker:/data 
  bigchaindb/bigchaindb 
  start`








