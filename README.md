# DBackup

## Usage
 - Simple tool to automatically export backups of databases
 - Copy `config.sample.yml` to `config.yml` and configure your backup settings
 - Build the container, mount the config file to /app/config.yml and run the container

## Supported Databases
 - mysql/mariadb
 - postgresql
 - mongodb
 - influxdb v1
 - sqlite (copy)

