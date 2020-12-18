# Reproducible pipeline from Twitter API using DVC

One short paragraph of project description

## Setup

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Download

Define what you need to download the software, typically through cloning.

```sh
git clone https://github.com/collab-uniba/PH_miner.git
git submodule init
git submodule update
```

### Configuration

Define a step-by-step series of examples that tell you how to configure and get a development environement running.

Number the steps as follows.

1. Create the file `db/cfg/dbsetup.yml` to setup the connection to the MySQL database:

```yaml
mysql:
    host: 127.0.0.1
    user: root
    passwd: *******
    db: databasename
    recycle: 3600
```

2. In the project root folder, create the file `credentials_miner.yml` with the following structure:

```yaml
api:
  key: CLIENT_KEY
  secret: CLIENT_SECRET
  redirect_uri: APP_REDIRECT_URI
  dev_token: DEVELOPER_TOKEN
```

3. Create a Python 3.7 virtual environment `venv` via [`virtualenv`](https://virtualenv.pypa.io/en/latest/) and install dependencies as listed in `requirements.txt`:

```sh
virtualenv -p /usr/bin/python3.7 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

To lauch the tool, from the terminal execute `run.sh`. Use the `-h|--help` flag to see help and CLI parameters:

```sh
sh phminer.sh -h

NAME
    phminer - Extracts daily posts from ProductHunt.com
SYNOPSIS
    sh phminer.sh [-h|--help] [-s|--start date] CSVFILE
DESCRIPTION
    Extracts daily posts from ProductHunt.com.

    Displays brief summaries of builtin commands. If PATTERN IS
    specified, gives detailed help on all commands matching PATTERN,
    otherwise the list of help topics is printed.

    Options:
      -h      | --help             output this menu
      -s date | --start date       mines posts since date (YYYY-MM-DD)

    Parameters:
      CSVFILE                      Comma-separated output file

    Exit Status:
    Returns success unless CSVFILE is missing, date is not well-formatted 
    as YYYY-MM-DD, or an invalid option is given.
```

### Examples

Mine posts since May 22, 2019 to date and save output into file `posts.csv`:

```sh
sh phminer.sh -s 2019-05-22 posts.csv
```

## Test cases execution

To execute unit test cases, run:

```sh
sh unit_tests.sh
```

Logs will be stored into text file `unit-tests-yyyy-mm-dd.log`.

## Deployment

A Docker container is specified via file `Dockerfile`. To build an image, execute:

```sh
docker build --no-cache -t collabuniba/hminer:vX Dockerfile
```

Note that `vX` should match the version number or omit `:Vx` to override the latest version.

To push it to DockerHub:

```sh
docker push collabuniba/phminer:Vx
```

For an interactive shell of the latest version, execute:

```sh
docker run --rm -it collabuniba/phminer
```

## Resources & Libraries

* Product Hunt [API](https://api.producthunt.com/v1/docs)
* [ph_py](https://github.com/anatg/ph_py) - ProductHunt.com API wrapper in Python
* [Scrapy](https://scrapy.org) - A scraping and web-crawling framework
* [Selenium](https://www.seleniumhq.org) - A suite of tools for automating web browsers
* [ChromeDriver](http://chromedriver.chromium.org) - Tool to connect to Chromium web browser
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/) - HTML parser

## Versions

We use [semantic versioning](http://semver.org/). For more on the versions available, see the [tags on this repository](https://github.com/your/project/tags).

* `0.2.0` - Add extraction of user reputation
* `0.1.1` - Fix bug in Docker deployment script
* `0.1.0` - Initial release

## Authors

* **[Fabio Calefato](https://github.com/PurpleBooth)** - Initial work and project maintenance
* ...

See also the full list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
