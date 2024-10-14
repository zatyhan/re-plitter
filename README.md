# 🎈 re-plitter

This web app is designed to ease your (or only me?) bill splitting problems, and most importantly - installation-free! 

How to use the app:

1. Insert as many names to the table whom you will be splitting the receipt with
2. Add the item value, item name and the people you are sharing it with
3. Press enter and get your splitted bill calculated in a jiffy! 

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run replitter.py
   ```

# Development
# To Dos:
- [x] add items column to list the items being shared among the parties
- [x] display items list together with their price and number of people to split with for sanity check
- [ ] add option of splitting option - equal or by percentage share 
- [ ] add percentage share feature 
- [ ] use of dynamic tags to edit the share 
   - not yet possible due to limitation on streamlit development
- [ ] add image upload for ease of input references
- [ ] cache the page 
- [ ] integrate receipt reader (very far in the future)