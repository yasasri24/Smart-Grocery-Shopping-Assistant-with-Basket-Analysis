import streamlit as st
import pandas as pd


# Main Streamlit app
def main():
    st.title('Grocery Genius: Smart Grocery Shopping Assistant')
    st.write('Select Groceries that you want to Buy')
    rules = pd.read_hdf('rules.h5', key='df')
    print('loaded')

    all_groceries = set()
    for itemset in rules['antecedents']:
        all_groceries.update(itemset)
    groceries=list(all_groceries)
    groceries.sort()
    # print(groceries)

    # Checkbox for selecting groceries
    selected_items = st.multiselect('Select groceries:', groceries)
    
    if st.button('Buy'):
        if len(selected_items) > 0:
            print(selected_items)
            recommended_items = set()
            for item in selected_items:
                recommendations = rules[rules['antecedents'] == {item}]['consequents']
                recommended_items.update(recommendations)
            st.success('You can also include these items to your Basket...!')
            print(recommended_items)
            for recomm in recommended_items:
                st.success(list(recomm)[0])

                
        else:
            st.warning('Please select at least one item.')

if __name__ == '__main__':
    main()
