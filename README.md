# Harvard's Artifacts Collection

An interactive, end-to-end ETL and data exploration platform built using the Harvard Art Museums public API.

This project collects artifact data from the Harvard Art Museums API, transforms the API responses into structured records, stores the data in MySQL, and provides an interactive Streamlit application to explore the collection and run SQL queries.

## Project Features

- **API Integration:** Collects artifact data from the Harvard Art Museums public API.
- **ETL Pipeline:** Extracts data from API responses, transforms it into structured records, and loads it into MySQL.
- **Data Transformation:** Organizes artifact information into metadata, media, and color records.
- **Database Design:** Stores the data in three MySQL tables: `artifact_metadata`, `artifact_media`, and `artifact_colors`.
- **Interactive Data Exploration:** Uses Streamlit to collect, display, and explore artifact data.
- **SQL Analytics:** Includes 25 predefined SQL queries covering artifact details, classifications, departments, media, rankings, and color analysis.

## Technologies Used

- Python
- Pandas
- Requests
- MySQL
- SQL
- Streamlit
- Harvard Art Museums API

## Database Tables

- `artifact_metadata` — Stores artifact details such as title, culture, period, medium, and classification.
- `artifact_media` — Stores image counts, media counts, color counts, and ranking information.
- `artifact_colors` — Stores color information associated with artifacts.

## Data Collected

The current dataset contains 10,000 artifact records across four classifications:

- Coins
- Paintings
- Sculpture
- Photographs

Each classification contains 2,500 artifact records.

## How to Run the Application

1. Install Python and the required packages.
2. Set up MySQL and create the required database.
3. Configure the Harvard API key and database credentials using environment variables in a `.env` file.
4. Open the project folder in the terminal.
5. Run the application:

   `streamlit run APP.py`

## What I Learned

Through this project, I gained practical experience working with API integration, data extraction and transformation, MySQL database design, SQL queries, and building an interactive application using Streamlit.
