#!/usr/bin/expect

# 3900w11ayellowfrogs

## Frontend

# This project with bootstrapped with Vite via:
### Install npm
sudo apt -y install npm

### Install yarn
# Recommend installing Yarn using npm (node packet manager) which can be installed alongside Node.js.
sudo npm install --global yarn 

### Install curL
sudo apt -y install curl 

### Install the correct nodejs
curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt-get install -y nodejs

### Install dependencies
# Required on initial installation and when adding any additional packages to the project.
cd frontend
yarn #

## Run frontend locally The following command should be run from the `frontend` directory
yarn dev
