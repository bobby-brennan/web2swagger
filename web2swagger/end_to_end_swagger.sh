#! /bin/bash

#git clone https://github.com/bobby-brennan/scrape-to-swagger.git
mkdir scrape-to-swagger ; true

cd scrape-to-swagger
npm install scrape-to-swagger
cd ..
python end_to_end_swagger.py ./config/$1.py ../../../config/$1.js results.json