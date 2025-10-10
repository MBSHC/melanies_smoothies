# Import python packages
import streamlit as st 
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col


# Function to get session
def get_session():
    try:
        return get_active_session()
    except Exception as e:
        st.warning("Running in local mode. Using manual session config.")
        connection_parameters = {
            "account": "MPUIHRC-STB70179",
            "user": "SHChu",
            "password": "xxxx",
            "role": "SYSADMIN",
            "warehouse": "COMPUTE_WH",
            "database": "SMOOTHIES",
            "schema": "PUBLIC"
        }
        return Session.builder.configs(connection_parameters).create()

# Get session
session = get_session()

# Write directly to the app
# if you're new to Streamlit,** check out our easy-to-follow guides at
# (https://docs.streamlit.io).
# App UI
st.title(f"Customize Your Smoothie! :cup_with_straw: ")
st.write(
  """Choose the fruits you want in your custom smoothie! 
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# session = get_active_session()  
# Load fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

# multiselect
ingredients_list = st.multiselect('Choose up to 5 ingredients:'
                                 , my_dataframe
                                 , max_selections=5
                                 )

if ingredients_list:
    #st.write (ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    st.write(my_insert_stmt) 
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        order_message = 'Your Smoothie is ordered, ' + name_on_order+ '!'
        st.success(order_message, icon="✅")

    
