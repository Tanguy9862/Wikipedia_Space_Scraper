# Wikipedia Space Scraper

## Overview

This Python package is designed to scrape historical space exploration data from the French version of Wikipedia. The data is automatically translated into English. It is part of a larger project, [Space-App](https://github.com/Tanguy9862/Space-App), which visualizes various aspects of space exploration.

## Features

- **Data Scraping**: Utilizes BeautifulSoup to scrape data tables from the French version of Wikipedia.
- **Automatic Translation**: Translates the scraped data from French to English.
- **Data Transformation**: Transforms the scraped data into a JSON format for easy consumption.
- **Error Handling**: Robust error handling to ensure data integrity.
- **Logging**: Detailed logging for debugging and monitoring.

## Installation

To install this package, run:

```bash
pip install git+https://github.com/Tanguy9862/Wikipedia_Space_Scraper.git
```

## Usage

After installation, you can import the package and use the `scrape_wikipedia_data()` function to scrape the data.

```python
from wikipedia_space_scraper import scraper

# Scrape Wikipedia data
scraper.scrape_wikipedia_data()
```

## Dependencies

- Python 3.x
- BeautifulSoup
- Requests
- Pandas

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Related Projects

- [Space-App](https://github.com/Tanguy9862/Space-App)
- [Next-Launch-Scraper](https://github.com/Tanguy9862/Next-Launch-Scraper)
- [NextSpaceFlight-Scrapper](https://github.com/Tanguy9862/NextSpaceFlight-Scrapper)
