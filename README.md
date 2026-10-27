# Harvard's Artifacts Collection

This is my Data Science project based on the Harvard Art Museums collection. I used the Harvard Art Museums API to collect artifact data, stored it in MySQL, and built a Streamlit app to explore the data and run SQL queries.

## What I worked on

- Collected artifact data from the Harvard Art Museums API.
- Worked with four classifications: Coins, Paintings, Sculpture, and Photographs.
- Separated the collected data into three tables: metadata, media, and colors.
- Connected Python with MySQL to store the data.
- Built a Streamlit app to collect and display artifacts and insert the data into MySQL.
- Added 25 SQL questions to explore the collection and understand the data better.

## Tools I used

- Python
- Streamlit
- MySQL
- Pandas
- Requests
- Harvard Art Museums API

## Database tables

- `artifact_metadata` – stores details such as title, culture, period, medium, and classification.
- `artifact_media` – stores image counts, media counts, color counts, and ranking information.
- `artifact_colors` – stores the color information associated with artifacts.

## Data collected

I collected 2,500 records from each of the four classifications, giving me a total of 10,000 artifact records.

## How to run the app

1. Install the required Python packages.
2. Set up MySQL and configure the database credentials and API key in the environment variables.
3. Open the project folder in the terminal.
4. Run the following command:

```bash
streamlit run APP.py
```

## What I learned

Through this project, I got practical experience working with APIs, handling data in Python, creating MySQL tables, inserting records, writing SQL queries, and building a simple web app using Streamlit.
