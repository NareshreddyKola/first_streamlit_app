import streamlit
import pandas as pd
import requests

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
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
#streamlit.text(fruityvice_response.json())

#normalize json response
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
#Render normalized fruityvice to a streamlit dataframe 
streamlit.dataframe(fruityvice_normalized)


