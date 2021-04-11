#  Importing libraries
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
# import matplotlib.pyplot as plty
# from matplotlib import style
import numpy as np
import streamlit as st


#  Importing the dataset. This data set is for an online retail shop, containing more than 100 thousand sales records for 1 year (2018-2019)
df = pd.read_csv("transaction_data.csv")


def clean_data(df):
    #  Cleaning data
    df = df[df.UserId > 0]
    df = df[df.ItemCode > 0]
    df = df[df.NumberOfItemsPurchased > 0]
    df = df[df.CostPerItem > 0]
    df = df[df.ItemDescription.notna()]
    df = df[df.TransactionTime.str[-4:] != '2028']
    return df


def encode(x):
    if x <= 0:
        return 0
    else:
        return 1


def toString(x):
    string = '' + str(x)
    string = string[12:-3:1]
    return string


def product_exist(prod):
    return prod in rules_list


def find_product_rules(product):
    if (product_exist(product) == True):
        results = rules[rules['antecedents'] == product]
        return results
    else:
        message = "Poduct has no basket yet"
        return message


df = clean_data(df)

# retrieving item names in the dataset
prod_des = df['ItemDescription'].unique()
item_list = ['']

for x in prod_des:
    item_list.append(x)

#  Re-arranged the dataframe into a matrix of products per transaction
df_set = df.groupby(['TransactionId', 'ItemDescription']).NumberOfItemsPurchased.sum(
).unstack().reset_index().fillna(0).set_index('TransactionId')

df_set = df_set.applymap(encode)

# Applied Apriori algorithm to get the frequently bought item-sets
frequent_itemsets = apriori(df_set, min_support=0.015, use_colnames=True)

# Applied the association rules on the item-sets
# Tuned the confidence minimum threshold to 0.2
rules = association_rules(
    frequent_itemsets, metric='confidence', min_threshold=0.20)

rules['antecedents'] = rules['antecedents'].apply(lambda x: toString(x))
rules['consequents'] = rules['consequents'].apply(lambda x: toString(x))

rules_list = rules["antecedents"].to_list()

# front end elements of the web page

html_temp = """ 
<div style ="background-color:#85c1ff;padding:13px"> 
<h1 style ="color:black;text-align:center;">Basket Analysis Web App</h1> 
</div> 
"""

st.markdown(html_temp, unsafe_allow_html=True)
input_product = st.selectbox("Search or Select product", item_list)

if (input_product):
    if (input_product == ''):
        st.write("Wrong input, kindly select a product from the list.")
    else:
        results = find_product_rules(input_product)
        st.write("Basket results")
        for i in results['consequents']:
            st.write(i)
