from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import mysql.connector

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="world"
)

cursor = db_connection.cursor()

# Clear all rows and replace the new one
cursor.execute("TRUNCATE population")

# Replace the path with the location of your Chrome WebDriver executable
webdriver_path = "C:\Portable Apps\chromedriver_win32"

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without opening a window)

# Create a WebDriver instance
driver = webdriver.Chrome(service=Service(webdriver_path), options=chrome_options)

url = "https://worldpopulationreview.com/"
driver.get(url)

# Wait for the table to load by checking for a specific element
driver.find_element(By.CSS_SELECTOR, ".jsx-a3119e4553b2cac7")

# Find the table that contains the population data
table = driver.find_element(By.CSS_SELECTOR, ".jsx-a3119e4553b2cac7")

# Find all rows in the table (excluding the header row)
rows = table.find_elements(By.TAG_NAME, "tr")[1:]

# Iterate over each row and extract the country name and population
for row in rows:
    columns = row.find_elements(By.TAG_NAME, "td")
    country = columns[0].text.strip()
    pop_2023 = columns[1].text.strip().replace(",","")
    pop_2022 = columns[2].text.strip().replace(",","")
    area = columns[3].text.strip()
    land_area = columns[4].text.strip()
    density = columns[5].text.strip().replace(",","")
    growth_rate = columns[6].text.strip()
    world_pct = columns[7].text.strip()
    
    print(country)
    print(pop_2023)
    print(pop_2022)
    print(area)
    print(land_area)
    print(density)
    print(growth_rate)
    print(world_pct)
    print("------------------------")

    # Prepare the INSERT INTO Query
    column_names = ["country", "pop_2023", "pop_2022", "area", "land_area", "density", "growth_rate", "world_pct"]
    values = [country, pop_2023, pop_2022, area, land_area, density, growth_rate, world_pct]

    # Generate placeholders for the values
    placeholders = ",".join(["%s"] * len(column_names))

    query = f"INSERT INTO population ({','.join(column_names)}) VALUES ({placeholders})"

    # Execute the query with the array values
    cursor.execute(query, values)

# Commit the changes to the database
db_connection.commit()

# Close the cursor and database connection
cursor.close()
db_connection.close()

driver.quit()

