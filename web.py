#  Importing libraries
import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

# the Main function
html_temp = """
<div style="background-color:#9932CC;padding:10px">
<h2 style="color:white; text-align:center;">Basket Analysis App</h2>
</div>
"""

st.markdown(html_temp, unsafe_allow_html=True)
product = st.text_input("Enter a product to generate basket", "")

#  Importing the dataset. This data set is for an online retail shop, containing more than 100 thousand sales records for 1 year (2018-2019)
datadf = pd.read_csv("transaction_data.csv")

df = datadf.copy()


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

st.success('The predicted category of the article is: {}'.format(result))
html_temp = """
<div style="background-color:grey;padding:6px">
<h6 style="color:white;">Other related articles</h3>
</div>
"""

st.button("Compute basket")
if st.button("Compute basket"):
    st.markdown(html_temp, unsafe_allow_html=True)
    st.write(find_product_rules(product))
