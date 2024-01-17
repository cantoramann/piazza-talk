import scrape
import post_loader

def main():
    # scrape.scrape()
    post_loader.setup_db()
    post_loader.run_search_loop()

main()