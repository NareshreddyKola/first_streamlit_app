import streamlit
import pandas as pd
import requests
import snowflake.connector

streamlit.title('My Parents New Healthy Dinner')

streamlit.header('Breakfast Favorites')

streamlit.text('🥣 Omega 3 & Blueberry Oat Meal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-boiled Free-range eggs')
streamlit.text('🥑🍞 Avocado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

myfruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
myfruit_list = myfruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect('Pick Some Fruits', list(myfruit_list.index), ['Avocado','Strawberries'])
fruits_show = myfruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_show)

streamlit.header('Fruityvice Fruit Advice!')
fruit_choice = streamlit.text_input('What Fruit information would you like information about?', 'kiwi')
streamlit.write('The Customer Entered', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#streamlit.text(fruityvice_response.json())

#normalize json response
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
#Render normalized fruityvice to a streamlit dataframe 
streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_data_row = my_cur.fetchone()
#streamlit.text(my_data_row)
#streamlit.text("Hello from Snowflake:")
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("My Fruit Load List contains:")
streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('What Fruit would you like to add?')
streamlit.write('The Customer Entered', add_my_fruit)
my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values(add_my_fruit)")
