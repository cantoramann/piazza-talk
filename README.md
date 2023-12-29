# Piazza Scraper README.md

## Overview

The Piazza Scraper is a tool designed for instructors to extract posts, questions, and other relevant information from Piazza, a popular Q&A platform used in academic settings. This script iterates through post IDs, collects data, and writes content to text files within a specified directory.

## Features

- Iterative post ID access
- Extraction of post details including title, type, content, answers, follow-ups, and tags
- Handling of private or inaccessible posts
- Error management and rate-limiting considerations

## Setup

Clone the repository or download the script to your local machine and ensure all dependencies listed in the script are installed.

### Install Packages

A Python environment with necessary packages installed. `pip install -r requirements.txt` will install the dependencies.

### Load Piazza Session Credentials

Valid session cookies and headers are needed for authenticated access to Piazza. These can be found simply by checking the Networking tab of your browser when you open your Piazza feed. Config file includes all the variables needed to run the program. These variables should be put into a `.env` file, and they are imported in `config.py`

Note that in `config.py`, the `referer` header is not included inside the `headers` object but independently as a `REFERER_BASE` variable. See the expected format in `config.py`. Also, make sure to export your `referer` header as `referer_base` or change `REFERER_BASE=os.environ.get('referer_base')` accordingly.

Additionally, you will also need the `nid` variable. For this, go to your Networking tab and load a page from your Piazza class. Click on the `method=content.get` url, go to Payload, and choose `nid` from your params.

After preparing your `.env` file, simply run `chmod +x envs.sh` and `source envs.sh` on your shell session, respectively.

Some cookie and header data are subject to change after extensive requests, but that is typically unlikely to be an issue given the average number of questions asked in a semester long class.

### Load Posts to Vector Database

To load the scraped posts into Weaviate, an `OPENAI_API_KEY` is used in `.env`, and it is directly imported in `db.py`. After that, run `docker compose up -d` and then `python db.py` to load the data into the containerized Weaviate database. Since the Weaviate container does not have a dedicated volume in the current `docker-compose.yml`, data will be lost when the container is stopped. This can be changed if desired by modifying `docker-compose.yml`

## Usage

Run the script with Python. Modify the script parameters as needed for your specific use case, such as changing the post ID range or handling rate limits more gracefully.

```bash
python main.py
```

As the script runs, it will access posts sequentially and write the data to text files in the specified directory. Monitor the output to ensure it's running as expected and handle any errors that might arise.

## License

This repository is under MIT License.
