#!/bin/bash

#read -p 'Please tell ur commit: ' com
echo 'Please tell ur commit: '
read words

git add .
git commit -m "$words"
git push