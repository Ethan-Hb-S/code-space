#!/usr/bin/expect

# 3900w11ayellowfrogs

## Backend

# Update system
sudo apt-get update

### Install pip
sudo apt -y install python3-pip

### Setup, create and activate the venv.
sudo apt install python3.8-venv
cd backend
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip3 install -r requirements.txt

### Setup postgresql
# From https://www.postgresql.org/download/linux/ubuntu/ \
# Enter the following lines in terminal one by one (not including the comments)
# Create the file repository configuration:
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

# Import the repository signing key:
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Update the package lists:
sudo apt-get update

# Install the latest version of PostgreSQL.
# If you want a specific version, use 'postgresql-12' or similar instead of 'postgresql':
sudo apt-get -y install postgresql

### Save user credentials to root
# https://www.youtube.com/watch?v=INJl3PLVZMo
sudo -u postgres psql

# The above will open up a psql terminal, enter the following:
# alter user postgres password 'lubuntu';

# Then type '\q' to exit the psql terminal (without the ' ')
psql -U postgres -h localhost

# When prompted enter 'lubuntu' as password (without the ' ')

# Then setup the database by typing:
# create database yellow_frogs;

# Then type '\q' to exit the psql terminal (without the ' ')

### Run the server
python3 app.py
