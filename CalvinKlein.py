#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np


# In[2]:


# Function to extract Product Title
def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("h1", attrs={"class":"product-name"})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

# Function to extract Product Price
def get_price(soup):

    try:
        price = soup.find("span", attrs={'class':"strike-through list"}).string.strip()

    except AttributeError:

        try:
            # If there is some deal price
            price = soup.find("span", attrs={'class':"sales body-font md"}).string.strip()

        except:
            price = ""

    return price

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("a", attrs={'class':"TTteaser__read-reviews"}).string.strip()

    except AttributeError:
        review_count = ""	

    return review_count

# Function to extract Star rating
def get_rating(soup):
    try:
        available = soup.find("div", attrs={'class':"TTteaser__rating"})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"	

    return available


# In[3]:


if __name__ == '__main__':

    #defining header
    HEADERS=({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36','Accept-Language':'en-US, en;q=0.5'})
    # The webpage URL
    URL = "https://www.calvinklein.us/en/women/apparel/denim?ab=w_visnav_denim"

    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class':"pdpurl"})

    # Store the links
    links_list = []

    # Loop for extracting links from Tag Objects
    for link in links:
            links_list.append(link.get('href'))

    d = {"title":[], "price":[], "rating":[], "reviews":[]}
    
     # Loop for extracting product details from each link 
    for link in links_list:
        new_webpage = requests.get("https://www.calvinklein.us/en" +link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Function calls to display all necessary product information
        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['reviews'].append(get_review_count(new_soup))

    
    ck_df = pd.DataFrame.from_dict(d)
    ck_df['title'].replace('', np.nan, inplace=True)
    ck_df = ck_df.dropna(subset=['title'])
    ck_df.to_csv("ck_data.csv", header=True, index=False)


# In[4]:


ck_df


# In[5]:


links_list


# In[6]:


for x in range(len(links_list)):
    print (links_list[x])


# In[7]:


for link in links:
            links_list.append(link.get('href'))


# In[8]:


links_list[1].get('href')


# In[ ]:





# In[ ]:





# In[ ]:




