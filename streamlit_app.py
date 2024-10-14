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
name= splitter.text_input('Name:', key="input_name", placeholder='Jane Doe')
error_text= splitter.empty()
submit_name= splitter.form_submit_button('Add person to the list')

if submit_name: 
    persons= add_splitter(name)

bills= st.form('bills', clear_on_submit=True)
running_total= bills.number_input('Item value', key='running_total', step=0.01, format="%0.2f", min_value=0.00, placeholder=0.00)
total_text= bills.empty()
item= bills.text_input('Which item is this for?', key='item', placeholder='water')
item_text= bills.empty()

if st.session_state.persons.empty:
    bills.write('')
else:
    bills.write('For who is this item is split among?')
for x in st.session_state.persons['Name']:
    if 'shareholders' not in st.session_state:
        st.session_state.shareholders=np.array([])
    if bills.checkbox(x):
        st.session_state.shareholders= np.append(st.session_state.shareholders, x)

shareholder_text= bills.empty()
split_item= bills.form_submit_button("Split this item!")

if split_item:
    # check whether item has a numeric value
    if running_total== 0 or running_total=='':
        total_text.write('**Did you forget to enter a value?**')
    else:
        # check whether item has a name
        if not st.session_state.item: 
            item_text.write('**Don\'t forget to put the item name!**')
        else: 
            # check whether database is empty
            if 'shareholders' not in st.session_state:
                bills.html("<p><span style='color: red; font-weight: bold;'>Error:</span> There's no one to share with &#128531</p>")
            else: 
                # check whether persons are selected
                if len(st.session_state.shareholders)==0:
                    shareholder_text.write('**Did you forget to select the person?**')
                else:
                    split_val= st.session_state.running_total/len(st.session_state.shareholders)
                    for shareholder in st.session_state.shareholders:
                        # st.write(shareholder)
                        st.session_state.persons.loc[st.session_state.persons['Name']==shareholder, 'Total'] += split_val
                        st.session_state.persons.loc[st.session_state.persons['Name']==shareholder, 'Items'].item().append(st.session_state.item)
    del st.session_state.shareholders
        
display= st.container()
if st.session_state.persons.empty:
    display.write("")
    display.html("<div style='font-weight: bold; font-size: 20px'> There\'s no one here yet &#128546 </div>")
else:
    display.dataframe(st.session_state.persons.round({'Total': 2}), hide_index=True, use_container_width=True)

if st.button("Reset calculator!"):
    del st.session_state.persons
    del st.session_state.shareholders

    st.rerun()
