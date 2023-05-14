# web-scraping-db-dataframe
For experiment purposes.

# install the ff libriaries below
# pip install pandas PyQt5 mysql-connector-python

# make sure you have to create the table with the ff mysql code
'''
CREATE TABLE IF NOT EXISTS population (
  id int NOT NULL AUTO_INCREMENT,
  country varchar(255) NOT NULL,
  pop_2023 int NOT NULL,
  pop_2022 int NOT NULL,
  area varchar(10) NOT NULL,
  land_area varchar(10) NOT NULL,
  density int NOT NULL,
  growth_rate decimal(5,2) NOT NULL,
  world_pct decimal(5,2) NOT NULL,
  datetime_added datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
)
'''
