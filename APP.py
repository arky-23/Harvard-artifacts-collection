
# ==========================================
# Harvard's Artifacts Collection
# ==========================================

# 1. Libraries
import os
import json
import time
import requests
import pandas as pd
import streamlit as st
import mysql.connector

from dotenv import load_dotenv
from mysql.connector import Error

# 2. Load configuration
load_dotenv()

API_KEY = os.getenv("HARVARD_API_KEY")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "harvard_art"),
}

# 3. Page configuration
st.set_page_config(
    page_title="Harvard's Artifacts Collection",
    page_icon="🏛️",
    layout="wide"
)

# 4. Application title
st.title("🎨 🏛️ Harvard’s Artifacts Collection")

st.write(
    "Explore artifacts from the Harvard Art Museums collection."
)


# 5. Database connection function
def get_db_connection():
    """Create and return a MySQL database connection."""
    return mysql.connector.connect(**DB_CONFIG)

# Create the three required SQL tables
def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifact_metadata (
            id INT PRIMARY KEY,
            title TEXT,
            culture TEXT,
            period TEXT,
            century TEXT,
            medium TEXT,
            dimensions TEXT,
            description TEXT,
            department TEXT,
            classification TEXT,
            accessionyear INT,
            accessionmethod TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifact_media (
            objectid INT PRIMARY KEY,
            imagecount INT,
            mediacount INT,
            colorcount INT,
            media_rank INT,
            datebegin INT,
            dateend INT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifact_colors (
            color_id INT AUTO_INCREMENT PRIMARY KEY,
            objectid INT,
            color VARCHAR(20),
            spectrum VARCHAR(20),
            hue VARCHAR(50),
            percent FLOAT,
            css3 VARCHAR(50),
            INDEX (objectid)
        )
    """)

    conn.commit()
    cursor.close()
def insert_artifacts(conn, metadata, media, colors):
    cursor = conn.cursor()

    try:
        metadata_sql = """
            INSERT INTO artifact_metadata
            (id, title, culture, period, century, medium, dimensions,
             description, department, classification, accessionyear,
             accessionmethod)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE id = id
        """

        metadata_values = [
            (
                r["id"], r["title"], r["culture"], r["period"],
                r["century"], r["medium"], r["dimensions"],
                r["description"], r["department"], r["classification"],
                r["accessionyear"], r["accessionmethod"]
            )
            for r in metadata
        ]

        if metadata_values:
            cursor.executemany(metadata_sql, metadata_values)

        media_sql = """
            INSERT INTO artifact_media
            (objectid, imagecount, mediacount, colorcount,
             media_rank, datebegin, dateend)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE objectid = objectid
        """

        media_values = [
            (
                r["objectid"], r["imagecount"], r["mediacount"],
                r["colorcount"], r["rank"], r["datebegin"],
                r["dateend"]
            )
            for r in media
        ]

        if media_values:
            cursor.executemany(media_sql, media_values)

        colors_sql = """
            INSERT INTO artifact_colors
            (objectid, color, spectrum, hue, percent, css3)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        colors_values = [
            (
                r["objectid"], r["color"], r["spectrum"],
                r["hue"], r["percent"], r["css3"]
            )
            for r in colors
        ]

        if colors_values:
            cursor.executemany(colors_sql, colors_values)

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()



# Insert collected data into SQL
st.subheader("Migrate to SQL")

if st.button("Insert collected data"):
    if not st.session_state.metadata:
        st.warning("Please collect artifacts before inserting.")
    else:
        connection = None

        try:
            connection = get_db_connection()

            create_tables(connection)

            insert_artifacts(
                connection,
                st.session_state.metadata,
                st.session_state.media,
                st.session_state.colors
            )

            st.success("Data inserted successfully!")

        except Error as error:
            st.error(f"MySQL insertion failed: {error}")

        finally:
            if connection and connection.is_connected():
                connection.close()





# 6. Harvard API collection

API_URL = "https://api.harvardartmuseums.org/object"

if "metadata" not in st.session_state:
    st.session_state.metadata = []

if "media" not in st.session_state:
    st.session_state.media = []

if "colors" not in st.session_state:
    st.session_state.colors = []

classification = st.text_input(
    "Enter a classification:",
    placeholder="Example: Coins"
)

if st.button("Collect data"):
    if not API_KEY:
        st.error("Harvard API key is missing. Check your .env file.")

    elif not classification.strip():
        st.warning("Please enter a classification.")

    else:
        selected_classification = classification.strip().title()

        metadata = []
        media = []
        colors = []

        try:
            with st.spinner(
                f"Collecting {selected_classification} artifacts..."
            ):
                for page in range(1, 26):
                    params = {
                        "apikey": API_KEY,
                        "size": 100,
                        "page": page,
                        "classification": selected_classification
                    }

                    response = requests.get(
                        API_URL,
                        params=params,
                        timeout=30
                    )
                    response.raise_for_status()

                    records = response.json().get("records", [])

                    if not records:
                        break

                    for record in records:
                        metadata.append({
                            "id": record.get("id"),
                            "title": record.get("title"),
                            "culture": record.get("culture"),
                            "period": record.get("period"),
                            "century": record.get("century"),
                            "medium": record.get("medium"),
                            "dimensions": record.get("dimensions"),
                            "description": record.get("description"),
                            "department": record.get("department"),
                            "classification": record.get("classification"),
                            "accessionyear": record.get("accessionyear"),
                            "accessionmethod": record.get("accessionmethod")
                        })

                        media.append({
                            "objectid": record.get("objectid"),
                            "imagecount": record.get("imagecount"),
                            "mediacount": record.get("mediacount"),
                            "colorcount": record.get("colorcount"),
                            "rank": record.get("rank"),
                            "datebegin": record.get("datebegin"),
                            "dateend": record.get("dateend")
                        })

                        for color in record.get("colors") or []:
                            colors.append({
                                "objectid": record.get("objectid"),
                                "color": color.get("color"),
                                "spectrum": color.get("spectrum"),
                                "hue": color.get("hue"),
                                "percent": color.get("percent"),
                                "css3": color.get("css3")
                            })

            st.session_state.metadata = metadata
            st.session_state.media = media
            st.session_state.colors = colors

            st.success(
                f"Collected {len(metadata)} {selected_classification} artifacts."
            )

        except requests.RequestException as error:
            st.error(f"Harvard API request failed: {error}")

        except (ValueError, KeyError) as error:
            st.error(f"Could not process the API response: {error}")


# 7. Display the collected data

if st.session_state.metadata:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Metadata")
        st.dataframe(
            pd.DataFrame(st.session_state.metadata),
            use_container_width=True
        )

    with col2:
        st.subheader("Media")
        st.dataframe(
            pd.DataFrame(st.session_state.media),
            use_container_width=True
        )

    with col3:
        st.subheader("Colours")
        st.dataframe(
            pd.DataFrame(st.session_state.colors),
            use_container_width=True
        )

# Temporary database connection test
if st.button("Test MySQL Connection"):
    connection = None

    try:
        connection = get_db_connection()
        create_tables(connection)
        st.success(
            "MySQL connection successful. Required tables are ready."
        )

    except Error as error:
        st.error(f"MySQL connection failed: {error}")

    finally:
        if connection and connection.is_connected():
            connection.close()




# 8. SQL Analysis Workspace

SQL_QUERIES = {
    "1. Byzantine artifacts from the 11th century": """
        SELECT id, title, culture, century, period
        FROM artifact_metadata
        WHERE century LIKE '%11th%'
          AND culture LIKE '%Byzantine%'
    """,

    "2. Unique cultures": """
        SELECT DISTINCT culture
        FROM artifact_metadata
        WHERE culture IS NOT NULL
        ORDER BY culture
    """,

    "3. Artifacts from the Archaic Period": """
        SELECT id, title, culture, period
        FROM artifact_metadata
        WHERE period LIKE '%Archaic%'
    """,

    "4. Titles by accession year, newest first": """
        SELECT title, accessionyear
        FROM artifact_metadata
        ORDER BY accessionyear DESC
    """,

    "5. Artifact count per department": """
        SELECT department, COUNT(*) AS artifact_count
        FROM artifact_metadata
        GROUP BY department
        ORDER BY artifact_count DESC
    """,

    "6. Artifacts with more than one image": """
        SELECT m.objectid, a.title, m.imagecount
        FROM artifact_media m
        LEFT JOIN artifact_metadata a ON a.id = m.objectid
        WHERE m.imagecount > 1
    """,

    "7. Average artifact rank": """
        SELECT AVG(media_rank) AS average_rank
        FROM artifact_media
    """,

    "8. Artifacts with more colors than media files": """
        SELECT objectid, colorcount, mediacount
        FROM artifact_media
        WHERE colorcount > mediacount
    """,

    "9. Artifacts created between 1500 and 1600": """
        SELECT a.id, a.title, m.datebegin, m.dateend
        FROM artifact_metadata a
        JOIN artifact_media m ON a.id = m.objectid
        WHERE m.datebegin >= 1500 AND m.dateend <= 1600
    """,

    "10. Artifacts with no media files": """
        SELECT COUNT(*) AS artifacts_without_media
        FROM artifact_media
        WHERE mediacount = 0
    """,

    "11. Distinct color hues": """
        SELECT DISTINCT hue
        FROM artifact_colors
        WHERE hue IS NOT NULL
        ORDER BY hue
    """,

    "12. Top five colors by frequency": """
        SELECT color, COUNT(*) AS frequency
        FROM artifact_colors
        WHERE color IS NOT NULL
        GROUP BY color
        ORDER BY frequency DESC
        LIMIT 5
    """,

    "13. Average color coverage by hue": """
        SELECT hue, AVG(percent) AS average_coverage
        FROM artifact_colors
        WHERE hue IS NOT NULL
        GROUP BY hue
        ORDER BY average_coverage DESC
    """,

    "14. Colors for a given artifact ID (example: 4617)": """
        SELECT objectid, color, spectrum, hue, percent, css3
        FROM artifact_colors
        WHERE objectid = 4617
    """,

    "15. Total number of color entries": """
        SELECT COUNT(*) AS total_color_entries
        FROM artifact_colors
    """,

    "16. Byzantine artifact titles and hues": """
        SELECT a.title, c.hue
        FROM artifact_metadata a
        JOIN artifact_colors c ON a.id = c.objectid
        WHERE a.culture LIKE '%Byzantine%'
    """,

    "17. Each artifact title with its hues": """
        SELECT a.title, c.hue
        FROM artifact_metadata a
        JOIN artifact_colors c ON a.id = c.objectid
        ORDER BY a.title
    """,

    "18. Titles, cultures and ranks where period exists": """
        SELECT a.title, a.culture, m.media_rank
        FROM artifact_metadata a
        JOIN artifact_media m ON a.id = m.objectid
        WHERE a.period IS NOT NULL AND a.period <> ''
    """,

    "19. Top 10 ranked artifacts with Grey hue": """
        SELECT a.title, m.media_rank, c.hue
        FROM artifact_metadata a
        JOIN artifact_media m ON a.id = m.objectid
        JOIN artifact_colors c ON a.id = c.objectid
        WHERE c.hue = 'Grey'
        ORDER BY m.media_rank ASC
        LIMIT 10
    """,

    "20. Artifact count and average media count per classification": """
        SELECT a.classification,
               COUNT(DISTINCT a.id) AS artifact_count,
               AVG(m.mediacount) AS average_media_count
        FROM artifact_metadata a
        LEFT JOIN artifact_media m ON a.id = m.objectid
        GROUP BY a.classification
        ORDER BY artifact_count DESC
    """,

    "21. Total number of artifacts": """
        SELECT COUNT(*) AS total_artifacts
        FROM artifact_metadata
    """,

    "22. Artifact count per classification": """
        SELECT classification, COUNT(*) AS artifact_count
        FROM artifact_metadata
        GROUP BY classification
        ORDER BY artifact_count DESC
    """,

    "23. Artifacts with missing culture": """
        SELECT id, title, classification
        FROM artifact_metadata
        WHERE culture IS NULL OR culture = ''
        LIMIT 100
    """,

    "24. Ten artifacts with the most images": """
        SELECT a.id, a.title, m.imagecount
        FROM artifact_metadata a
        JOIN artifact_media m ON a.id = m.objectid
        ORDER BY m.imagecount DESC
        LIMIT 10
    """,

    "25. Ten most frequent color hues": """
        SELECT hue, COUNT(*) AS frequency
        FROM artifact_colors
        WHERE hue IS NOT NULL
        GROUP BY hue
        ORDER BY frequency DESC
        LIMIT 10
    """
}

st.subheader("SQL Analysis Workspace")

selected_query = st.selectbox(
    "Choose an analysis question",
    list(SQL_QUERIES.keys())
)

if st.button("Run Query"):
    connection = None
    try:
        connection = get_db_connection()

        query = SQL_QUERIES[selected_query]

        result_df = pd.read_sql(query, connection)

        st.success("Query executed successfully!")
        st.dataframe(result_df, width="stretch")

        st.caption(f"Rows returned: {len(result_df)}")

    except Exception as error:
        st.error(f"Query failed: {error}")

    finally:
        if connection and connection.is_connected():
            connection.close()

