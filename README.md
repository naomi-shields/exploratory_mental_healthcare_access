# Exploring Mental Health Care Access in the United States
## Using the CDC's National Health and Nutrition Examination Survey responses, this analysis explores mental health care access in the United States. 
### The Data
All of the data used in this analysis can be found on the CDC's website [here](https://wwwn.cdc.gov/nchs/nhanes/search/DataPage.aspx?Component=Questionnaire&Cycle=2017-2020). Out of all of the National Health and Nutrition Examination datasets, the following were utilized in this analysis:
* P_HIQ: provides health insurance information
* P_HUQ: provides access to care information
* P_INQ: provides income and poverty information
* P_DPQ: provides mental health screening information
### The Analysis
In order to perform the analysis, I used the pandas and sqlite3 packages in Python. Pandas was used to read in and merge the data and sqlite3 was used with SQL queries to retrieve information from the dataset.

I first queried to see what percentages if people had or hadn't seen a mental health provider based on their poverty index and insurance status. Overall, there were not drastic differences between the groups, but within each poverty index category the group without insurance always had a higher percentage of people that had not seen a mental health provider. The most notable difference was in the poverty index category of Below 1.0 where 85% of people with insurance had not seen a provider and 91% of people without insurance had not seen a provider. 
![seen provider percentages](/artifacts/seen_provider_percentages.png)

Next, I queried to investigate the breakdown of mental health sytmptoms grouped by whether or not the respondent had seen a mental health professional. The output below shows that there is very little variability between the groups.
![mental health symptoms](/artifacts/mental_health_perc.png)

To wrap up this preliminary analysis, I queried for the count and percentage of suicidal thoughts grouped by whether or not the respondent had seen a mental health professional. This showed that a little over 1% of the respondent had experienced suicidal thoughts, but had not been seen by a mental health professional. 
![suicidal breakdown](/artifacts/suicidal_count.png)
### Final Thoughts 
This analysis provides a preliminary look into mental health care access in the United States, highlighting the relationships between poverty, insurance status, and mental health symptoms. While the differences in provider access across poverty index categories were not drastic, the trend of uninsured individuals being less likely to see a mental health provider was consistent. Additionally, the prevalence of mental health symptoms appeared similar regardless of whether respondents had seen a provider, which may suggest barriers beyond financial or insurance-related factors, such as stigma, availability of services, or personal choice.

One of the more concerning findings is that over 1% of respondents reported experiencing suicidal thoughts without having seen a mental health professional. This underscores the importance of improving mental health outreach and accessibility, especially for vulnerable populations.

It is important to note that this dataset represents pre-pandemic data, and it is likely that mental health conditions have worsened since then due to the stressors of the COVID-19 pandemic. The impact of the pandemic on mental health, including increased rates of anxiety, depression, and suicidal ideation, calls for further analysis with more recent data to assess the current state of mental health care access.

Future analyses could explore additional factors such as regional differences or racial and ethnic disparities. Further investigation into reasons for not seeking care could provide deeper insights into potential interventions to improve access and support for those in need.

