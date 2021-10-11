from utils.webscrapper import Web_Scrapper

def main():
    scrapper = Web_Scrapper()
    national_src, summary_df = scrapper.scrape_summary("medal-standings.htm")
    print(summary_df)
    scrapper.scrape_country(national_src)
    single_USA = scrapper.get_country_df("United States of America")
    print(single_USA)


main()