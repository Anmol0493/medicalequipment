# Medical Equipment Scraper

This Python script is designed to scrape product information from a medical equipment website. It utilizes BeautifulSoup for web scraping and multithreading for efficient data extraction from multiple product categories simultaneously.

## Prerequisites

Before using this script, ensure that you have the following prerequisites in place:

- **Python**: Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

- **Required Libraries**: Install the necessary Python libraries by running the following command:

    ```bash
    pip install requests beautifulsoup4
    ```

## How to Use

1. Clone or download this repository to your local machine.

2. Open a terminal or command prompt and navigate to the directory containing the script files.

3. Look for `main.py` in the directory.

4. Edit the `url` variable in `main.py` to specify the URL of the medical equipment website you want to scrape.

5. Run the script by executing the following command:

    ```bash
    python main.py
    ```

6. The script will scrape product information from the specified website and save the data in the `Output.json` file in the same directory.

## Customization

- **URL**: Modify the `url` variable in `main.py` to point to the desired medical equipment website.

- **Multithreading**: The script utilizes multithreading for faster scraping. You can adjust the number of threads in the `run_multiThread` method within `main.py` to optimize performance based on your system capabilities.

- **Data Extraction**: Customize the `Scrap` method in `main.py` to extract specific product information as per your requirements. You can modify the parsing logic to capture additional details or exclude certain data points.

- **Error Handling**: Implement error handling mechanisms as needed to handle cases such as failed HTTP requests or unexpected page structures.

## Data Output

- **Output.json**: Contains the scraped product information in JSON format, including details such as product names, prices, model numbers, and image URLs.

## Notes

- Ensure compliance with the website's terms of service and robots.txt file when scraping data.

- Consider incorporating proxy rotation or IP rotation mechanisms to avoid IP bans or rate limiting from the website server.

- Regularly check and update the scraping logic to adapt to any changes in the website's HTML structure or content presentation.
