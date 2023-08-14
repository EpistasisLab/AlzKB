# Alzheimer's Knowledgebase (AlzKB) Site
This repository is comprised of the following components:

- **Website**: site with some general information about this project. The source code for this website is found in the `app` directory

- **Neo4j**: used to store the graph database for this Knowledgebase.

- **Nginx**: used as a reverse proxy for the Website and the Neo4j Browser

- **Docker Compose files**
  - The `.yml` files contain definitions for building a docker image.  

- **Environmental Variables**
  - The environmental variables in .env_sample are used by the different docker services.

# Installation
## Prerequisites
**Docker**
- Automated Installation
  - Run `install-docker.sh` to install **Docker Engine**
- Manual Installation
  - Install either [**Docker Desktop**](https://www.docker.com/products/docker-desktop/) or [**Docker Engine**](https://docs.docker.com/engine/getstarted/step_one/) based on your needs.
  - [**Docker Compose**](https://docs.docker.com/compose/install/)
## Building and Running
### Building and deploying all services
1. Get a dump file of the database [here](https://upenn.box.com/s/dalcofa8i7rkkc2h2n6bfg8nvmwi83pq) and put this file in **neo4j/dump/**, make sure the filename is alzkb.dump (rename it if necessary)
2. Copy the **.env_sample** as **.env** and set the variable values as needed for your environment.
3. **On the very first run**, uncomment the lines for the neo4j-admin service in the docker-compose.yml file, after the first run, the neo4j-admin service is not needed.
4. To deploy the Website, Neo4j, Nginx and dump the database into neo4j run: `docker compose up -d --build`
### Building and deploying the services independently
The services can be built independently of each other as needed.  
**First**, copy the **.env_sample** as **.env** and update the variable values as needed for your environment.
- Website
  - Run `docker compose -f ./app.yml up -d --build`
- Load the database dump
  1. Ensure that the neo4j docker container is not running, it must be stopped if it is.
  2. Get a dump file of the database [here](https://upenn.box.com/s/dalcofa8i7rkkc2h2n6bfg8nvmwi83pq) and put this file in **neo4j/dump/**, make sure the filename is alzkb.dump (rename it if necessary)
  3. Run `docker compose -f ./neo4j-admin.yml up -d --build`
- Neo4j
  - Run `docker compose -f ./neo4j.yml up -d --build`
- Nginx
  - Run `docker compose -f ./nginx.yml up -d --build`
## Environmental Variables
The **.env_sample** file contains the following environmental variables:
- `COMPOSE_PROJECT_NAME` Base name of this project.
  - See the docker [documentation](https://docs.docker.com/compose/reference/envvars/) for more details.
- `ALZKB_HOST` IP address (or URL) of the host server where the **Website** will be deployed.
- `ALZKB_NEO4J_BROWSER` URL used for the Neo4J Browser, (may be different from `ALZKB_HOST`)
- `ALZKB_APP_SERVICE` Name of the docker service where the **Website** will run. This value is used by Nginx to forward requests to this service.
- `ALZKB_PORT` Port used by ExpressJS to serve the **Website**, Nginx will forward requests to `ALZKB_HOST` to this port.
- `ALZKB_DATA_ROOT` Directory where the data from **Neo4J** will be stored on the host machine (data, logs, etc.)
- `NEO4J_*` variables to configure Neo4j
  - For more information about these varibales, see the neo4j.conf [documenation](https://neo4j.com/docs/operations-manual/5/configuration/neo4j-conf/).
  - More details about how these variables map to the neo4j.conf file can be found [here](https://neo4j.com/docs/operations-manual/current/docker/configuration/)
- `NODE_ENV` Set to either **prod** or **dev** 
  - see [here](https://docs.npmjs.com/cli/v8/commands/npm-install) for more details.
