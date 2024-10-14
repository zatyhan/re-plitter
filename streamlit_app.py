import streamlit as st
import numpy as np
import pandas as pd

st.title("Receipt splitter (**:star: re-plitter :star:**)")
st.write(
    "This micro app is designed to ease your receipt bill splitting problem!" )

if 'temp' not in st.session_state:
    st.session_state["temp"]= ""
if 'persons' not in st.session_state:
    st.session_state.persons= pd.DataFrame({"Name": [], 
                            "Items": [],
                            "Total": []})
if 'item_list' not in st.session_state:
    st.session_state.item_list= pd.DataFrame({'Item': [], 
                                          'Number of people to split with': [],
                                          'Item amount': []})

def add_splitter(name):
    # splitter.write('jenny' in st.session_state.persons.values)
    if name not in st.session_state.persons.values and name.strip()!= '':
        person= pd.DataFrame({"Name": [name], "Items":[[]], "Total": [float(0.00)]})
        st.session_state.persons= pd.concat([st.session_state.persons, person], ignore_index=True)
        # st.write(persons)
    elif name.strip() == '' :
        error_text.write('**Did you forget to put a name?**')
    else:
        error_text.write(f'**{name}** is already in the list')

splitter= st.form('splitters', clear_on_submit=True)
name= splitter.text_input('Name', key="input_name", placeholder='Jane Doe', help='Name of the person you are splitting with')
error_text= splitter.empty()
submit_name= splitter.form_submit_button('Add person to the list')

if submit_name: 
    persons= add_splitter(name)

bills= st.form('bills', clear_on_submit=True)
running_total= bills.number_input('Item value', key='running_total', step=0.01, format="%0.2f", min_value=0.00, placeholder=0.00, help='Value of the item your are splitting')
total_text= bills.empty()
item= bills.text_input('Which item is this for?', key='item', placeholder='water')
item_text= bills.empty()

if st.session_state.persons.empty:
    bills.write('')
else:
    bills.write('Who is this item is split among?')
for x in st.session_state.persons['Name']:
    if 'shareholders' not in st.session_state:
        st.session_state.shareholders=set()
    if bills.checkbox(x):
        st.session_state.shareholders.add(x)

shareholder_text= bills.empty()
split_item= bills.form_submit_button("Split this item!")

if split_item:
    # check whether item has a numeric value
    if running_total== 0 or running_total=='':
        total_text.html("<p style='color: #dc143c; font-weight: bold;'>Did you forget to enter a value?</p>")
    else:
        # check whether item has a name
        if not st.session_state.item: 
            item_text.html("<p style='color: #dc143c; font-weight: bold;'>Don't forget to put the item name!</p>")
        else: 
            # check whether database is empty
            if 'shareholders' not in st.session_state:
                bills.html("<p><span style='color: #dc143c; font-weight: bold;'>Error:</span> There's no one to share with &#128531</p>")
            else: 
                # check whether persons are selected
                if len(st.session_state.shareholders)==0:
                    shareholder_text.html("<p style='color: #dc143c; font-weight: bold;'>Did you forget to select the person?</p>")
                else:
                    # save the item in items df
                    item_detail= pd.DataFrame({'Item': [st.session_state.item], 
                                        'Number of people to split with': [len(st.session_state.shareholders)],
                                        'Item amount': [st.session_state.running_total]})
                    st.session_state.item_list = pd.concat([st.session_state.item_list, item_detail], ignore_index=True)
                    split_val= st.session_state.running_total/len(st.session_state.shareholders)
                    for shareholder in st.session_state.shareholders:
                        st.session_state.persons.loc[st.session_state.persons['Name']==shareholder, 'Total'] += split_val
                        st.session_state.persons.loc[st.session_state.persons['Name']==shareholder, 'Items'].item().append(st.session_state.item)
                del st.session_state.shareholders
        
display= st.container()
if st.session_state.persons.empty:
    display.write("")
    display.html("<div style='font-weight: bold; font-size: 20px'> There\'s no one here yet &#128546 </div>")
else:
    # reset the index
    st.session_state.item_list.index= st.session_state.item_list.index + 1
    st.session_state.persons.index= st.session_state.persons.index + 1 
    display.subheader('List of items')
    display.dataframe(st.session_state.item_list, use_container_width=True)

    display.subheader('Sharers')
    display.dataframe(st.session_state.persons.round({'Total': 2}), use_container_width=True)

if st.button("Reset calculator!"):

    if 'persons' in st.session_state :
        del st.session_state.persons 
    if 'shareholders' in st.session_state:
        del st.session_state.shareholders   
    if 'item_list' in st.session_state:
        del st.session_state.item_list  
    st.rerun()
