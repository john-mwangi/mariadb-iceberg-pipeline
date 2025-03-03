# This Makefile performs a clean rebuild of MediaWiki

all: docker_services update_mediawiki

UPDATE_CMD = php maintenance/run.php install --dbname=my_database --dbuser=my_user --dbpass=my_password --dbserver=mariadb-main \
--server="$${MW_SERVER}" --scriptpath="$${MW_SCRIPT_PATH}" --lang en \
--pass $${MEDIAWIKI_PASSWORD} mediawiki $${MEDIAWIKI_USER}

SETTINGS = \$$wgDBname = 'my_database';\n\
\$$dockerMainDb = [\n\
	\t'host' => 'mariadb-main',\n\
	\t'dbname' => 'my_database',\n\
	\t'user' => 'root',\n\
	\t'password' => 'main_root_password',\n\
	\t'type' => 'mysql',\n\
	\t'flags' => DBO_DEFAULT,\n\
	\t'load' => 0,\n\
];\n\
\$$dockerReplicaDb = [\n\
	\t'host' => 'mariadb-replica',\n\
	\t'dbname' => 'my_database',\n\
	\t'user' => 'root',\n\
	\t'password' => 'main_root_password',\n\
	\t'type' => 'mysql',\n\
	\t'flags' => DBO_DEFAULT,\n\
	\t'max lag' => 60,\n\
	\t'load' => 1,\n\
];\n\
// Integration tests fail when run with replication, due to not having the temporary tables.\n\
if ( !defined( 'MW_PHPUNIT_TEST' ) ) {\n\
	\t\$$wgDBservers = [ \$$dockerMainDb, \$$dockerReplicaDb ];\n\
} else {\n\
	\t\$$wgDBserver = \$$dockerMainDb['host'];\n\
	\t\$$wgDBuser = \$$dockerMainDb['user'];\n\
	\t\$$wgDBpassword = \$$dockerMainDb['password'];\n\
	\t\$$wgDBtype = \$$dockerMainDb['type'];\n\
}

docker_services: docker-compose.yml
	docker compose down
	docker system prune --all --force
	docker volume prune --all --force
	docker compose up -d

update_mediawiki: .env
	docker compose exec mediawiki composer update
	rm -f LocalSettings.php
	@until docker compose exec -ti mediawiki sh -c '$(UPDATE_CMD)'; do \
		echo "Update command failed. Retrying..."; \
		sleep 5; \
		done
	echo "$(SETTINGS)" >> LocalSettings.php

