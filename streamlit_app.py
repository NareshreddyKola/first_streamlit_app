import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

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

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    #streamlit.text(fruityvice_response.json())
    #normalize json response
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

streamlit.header('Fruityvice Fruit Advice!')
try: 
    fruit_choice = streamlit.text_input('What Fruit information would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information!")
    else:
        fruityvice_normalized_from_function = get_fruityvice_data(fruit_choice)
        #Render normalized fruityvice to a streamlit dataframe 
        streamlit.dataframe(fruityvice_normalized_from_function)
except URLError as e:
    streamlit.error()


def get_fruit_load_list():
    my_cur = my_cnx.cursor()
    #my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
    #my_data_row = my_cur.fetchone()
    #streamlit.text(my_data_row)
    #streamlit.text("Hello from Snowflake:")
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

streamlit.header("My Fruit Load List contains:")
#Button to deal with Fruit Load List
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('What Fruit would you like to add?')
streamlit.write('The Customer Entered', add_my_fruit)
#my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values('from streamlit')")
