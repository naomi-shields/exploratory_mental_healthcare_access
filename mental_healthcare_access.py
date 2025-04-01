#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd
import pyreadstat
import sqlite3


# In[7]:


# Reading in .xpt files
income,_ = pyreadstat.read_xport("P_INQ.xpt")
insurance,_ = pyreadstat.read_xport("P_HIQ.xpt")
utilization,_ = pyreadstat.read_xport("P_HUQ.xpt")
screening,_ = pyreadstat.read_xport("P_DPQ.xpt")


# In[9]:


# renaming the columns for clarity
income_df = income[["SEQN", "INDFMMPI","INDFMMPC"]].rename(
    columns={"SEQN": "respondent", "INDFMMPI": "poverty_index", "INDFMMPC": "poverty_cat"})
insurance_df = insurance[["SEQN", "HIQ011"]].rename(
    columns={"SEQN": "respondent", "HIQ011": "has_insurance"})
utilization_df = utilization[["SEQN", "HUQ090"]].rename(
    columns={"SEQN": "respondent", "HUQ090": "seen_mental_health"})
screening_df = screening[["SEQN", "DPQ010", "DPQ020", "DPQ060", "DPQ070", "DPQ100", "DPQ090"]].rename(
    columns={"SEQN": "respondent", "DPQ010": "little_interest", "DPQ020": "feeling_down", 
             "DPQ060" :"feel_bad_self", "DPQ070": "trouble_concentrating", "DPQ090": "suicidal",
             "DPQ100": "difficulty_caused"})


# In[10]:


# Merging datasets using left join
merged_df = (
    income_df
    .merge(insurance_df, on="respondent", how="left")
    .merge(utilization_df, on="respondent", how="left")
    .merge(screening_df, on="respondent", how="left")
)

# Display first few rows
print(merged_df.head())


# In[12]:


# Creating SQlite database for my use
conn = sqlite3.connect('temp_database.db')
cursuor = conn.cursor()

# saving merged_df to the database
merged_df.to_sql("merged_table", conn, if_exists= "replace", index= False)


# In[22]:


# querying for percentages of people that have or haven't seen a mental health provider 
# and grouping by their poverty index and insurance status
query = """
SELECT 
    CASE 
        WHEN poverty_index < 1 THEN 'Below 1.0'
        WHEN poverty_index <= 2 THEN '1.0 - 2.0'
        WHEN poverty_index <= 3 THEN '2.0 - 3.0'
        WHEN poverty_index <= 4 THEN '3.0 - 4.0'
        WHEN poverty_index <= 5 THEN '4.0 - 5.0' 
        
    END AS poverty_category,
    
    CASE 
        WHEN has_insurance = 1 THEN 'Yes'
        WHEN has_insurance = 2 THEN 'No'
    END AS insurance_status,

    COUNT(*) AS total_count,
    SUM(CASE WHEN seen_mental_health = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS perc_seen_provider,
    SUM(CASE WHEN seen_mental_health = 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS perc_not_seen_provider

FROM merged_table
WHERE seen_mental_health IN (1,2) AND has_insurance IN (1,2)  -- Exclude refused/don't know/missing values
GROUP BY poverty_category, insurance_status
ORDER BY 
    CASE 
        WHEN poverty_category = 'Below 1.0' THEN 1
        WHEN poverty_category = '1.0 - 2.0' THEN 2
        WHEN poverty_category = '2.0 - 3.0' THEN 3
        WHEN poverty_category = '3.0 - 4.0' THEN 4
        WHEN poverty_category = '4.0 - 5.0' THEN 5
    END;
"""


seen_provider_percentages = pd.read_sql_query(query, conn)
seen_provider_percentages


# In[25]:


# querying for percentage of mental health symptoms grouped by whether or not they've seen a mental health professional
query = """
SELECT 
    CASE 
        WHEN seen_mental_health = 1 THEN 'Yes'
        WHEN seen_mental_health = 2 THEN 'No'
    END AS seen_mental_health_pro,
    SUM(CASE WHEN little_interest IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS perc_little_interest,
    SUM(CASE WHEN feeling_down IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS perc_feeling_down,
    SUM(CASE WHEN feel_bad_self IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS perc_feel_bad_self,
    SUM(CASE WHEN trouble_concentrating IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS perc_trouble_concentrating
FROM merged_table
WHERE seen_mental_health IN (1,2)  -- Exclude missing/refused responses
GROUP BY seen_mental_health
ORDER BY seen_mental_health;
"""
mental_health_perc = pd.read_sql_query(query, conn)
mental_health_perc


# In[26]:


# queryinf for count of suicidal thoughts grouped by whether or not they've seen a mental health professional
query = """
SELECT 
    CASE 
        WHEN seen_mental_health = 1 THEN 'Yes'
        WHEN seen_mental_health = 2 THEN 'No'
    END AS seen_mental_health_pro,
    COUNT(*) AS total_count,
    SUM(CASE WHEN suicidal = 1 THEN 1 ELSE 0 END) AS num_suicidal,
    SUM(CASE WHEN suicidal = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS perc_suicidal
FROM merged_table
WHERE seen_mental_health IN (1,2)  -- Exclude missing/refused responses
GROUP BY seen_mental_health
ORDER BY seen_mental_health;
"""
suicidal_count = pd.read_sql_query(query, conn)
suicidal_count


# In[27]:


conn.close()


# In[ ]:




