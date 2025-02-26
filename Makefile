# This Makefile rebuilds MediaWiki

all: docker_services update_mediawiki

UPDATE_CMD = php maintenance/run.php install --dbname=my_database --dbuser=my_user --dbpass=my_password --dbserver=mariadb-main \
--server="$${MW_SERVER}" --scriptpath="$${MW_SCRIPT_PATH}" --lang en \
--pass $${MEDIAWIKI_PASSWORD} mediawiki $${MEDIAWIKI_USER}

SETTINGS = \$$wgDBname = 'my_database';\n\
\$$dockerMainDb = [\n\
	'host' => "mariadb-main",\n\
	'dbname' => 'my_database',\n\
	'user' => 'root',\n\
	'password' => 'main_root_password',\n\
	'type' => "mysql",\n\
	'flags' => DBO_DEFAULT,\n\
	'load' => 0,\n\
];\n\
\$$dockerReplicaDb = [\n\
	'host' => "mariadb-replica",\n\
	'dbname' => 'my_database',\n\
	'user' => 'root',\n\
	'password' => 'main_root_password',\n\
	'type' => "mysql",\n\
	'flags' => DBO_DEFAULT,\n\
	'max lag' => 60,\n\
	'load' => 1,\n\
];\n\
// Integration tests fail when run with replication, due to not having the temporary tables.\n\
if ( !defined( 'MW_PHPUNIT_TEST' ) ) {\n\
	\$$wgDBservers = [ $dockerMainDb, $dockerReplicaDb ];\n\
} else {\n\
	\$$wgDBserver = $dockerMainDb['host'];\n\
	\$$wgDBuser = $dockerMainDb['user'];\n\
	\$$wgDBpassword = $dockerMainDb['password'];\n\
	\$$wgDBtype = $dockerMainDb['type']\n\
}

docker_services: docker-compose.yml
	docker compose down
	docker system prune --all --force
	docker volume prune --all --force
	docker compose up -d

update_mediawiki: .env
	docker compose exec mediawiki composer update
	rm -f LocalSettings.php
	@echo "Running update command..."
	@until docker compose exec -ti mediawiki sh -c '$(UPDATE_CMD)'; do \
		echo "Update command failed. Retrying..."; \
		sleep 5; \
	done
	echo "$(SETTINGS)" >> LocalSettings.php

