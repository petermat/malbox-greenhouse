

sudo apt update
sudo apt install -y postgresql postgresql-contrib

# todo: edit sudo nano /etc/postgresql/10/main/conf.d/a.conf
# vagrant@malbox-logger:~$ sudo nano /etc/postgresql/10/main/pg_hba.conf

sudo -u postgres psql -U postgres -d postgres -c "alter user postgres with password 'postgres';"
sudo -u postgres createdb greenhouse