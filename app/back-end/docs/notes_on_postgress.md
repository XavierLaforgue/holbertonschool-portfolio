# Notes on `postgress`
<!-- TODO: write bash script to initialize the `postgres` database using the variables in the .env file -->
## Installation
To install and update `postgreSQL` using the official `postgreSQL` repository and not just the Ubuntu one:
```bash
sudo apt install -y postgresql-common
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
```
## Connection
The default is that only the `postgres` user may connect to the database server and perform administrator tasks.
The `postgres` user has no passsword, to connect to it we must, therefore, become that user before calling `psql`
```bash
sudo -u postgres psql
```
From the psql terminal we may create databases
We must now create a user
```bash
export $(grep '^DB_USER=' .env.dev)
sudo -u postgres createuser --login --no-superuser --no-createdb --no-createrole $DB_USER
```
We can confirm the currently existing roles (users) with
```bash
sudo -u postgres psql -c "\du"
```
To assign a password to the new user
```bash
export $(grep '^DB_PW=' .env.dev)
sudo -u postgres psql -v ON_ERROR_STOP=1 -c "ALTER ROLE $DB_USER WITH PASSWORD '$DB_PW';"
```
<!-- TODO: create database -->
<!-- TODO: change ownership of the database to the django user -->
## References
- [postgresql.org/download/linux/ubuntu/](https://www.postgresql.org/download/linux/ubuntu/)
- [https://doc.ubuntu-fr.org/postgresql](https://doc.ubuntu-fr.org/postgresql)
- [https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-20-04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-20-04)
<!-- TODO: consider trying [https://www.pgmodeler.io/](https://www.pgmodeler.io/) -->
