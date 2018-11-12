# Setup Instructions #
*(for Linux / Ubuntu only)*

## Requirements: ##
- Python 2.7
- Scrapy 1.0 or newer - Installation guide: http://doc.scrapy.org/en/latest/intro/install.html
- Other libraries as specified in requirements.txt should be installed by changing to the directory of the scraper where the requirements.txt resides and calling there *pip install -r requirements.txt*

Everything was tested on Ubuntu 16.04 LTS and will most probably work on all other Debian based Linux distributions. The scripts itself should run also on other Linux distributions, Mac and Windows, but the setup instructions might slightly deviate from the following steps.

### Setup Instructions ###
1. Fix potential problems with locale (if logging in from a non English / US system):

	> *sudo apt-get install language-pack-id*

	> *sudo dpkg-reconfigure locales*

2. Install python

	> *sudo apt-get install python python-pip*

3. Change to the directory of the scrapy project (where the scrapy.cfg resides)

4. Run *pip install -r requirements.txt*

## Usage ##
After setup you can run the crawler using these steps:

1. Change to the directory of the project (where the scrapy.cfg resides) and there run:

	> *scrapy crawl web2swagger -a config_file='config_file.py'*

	Example:

	> *scrapy crawl web2swagger -a config_file=web2swagger/config/basecamp.py*

This will start scraping the REST API into swagger format. Results will be validated and stored in a file named specs.json. 

For test and debugging purposes you can output the results into other formats and files by adding a *-o <filename>* to the command line. The different output formats can be activated by using the respective file ending for the output file name: CSV (file ending .csv), JSON (file ending .js), JSON-Lines (file ending .jl), XML (file ending .xml)

