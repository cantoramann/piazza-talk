import scrape
import db

def main():
    scrape.scrape()
    db.setup_db()
    db.run_search_loop()