from unicodedata import name
import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import numpy as np
import json

max_date = datetime.today()
skill_list = [
    '.NET', '.NET Core', 'Active Directory', 'AI', 'Algorithms', 'Android',
    'Angular', 'Ansible', 'APIs', 'AutoCAD', 'Automated Testing', 'AWS',
    'Azure', 'BDD', 'Big Data', 'Business Intelligence', 'C', 'C#', 'C++',
    'CAD', 'CD', 'Cisco', 'Cloud Platforms', 'Code Reviews', 'Confluence',
    'Continuous Integration', 'CRM', 'CSS', 'Data Analysis', 'Data Modeling',
    'Data Science', 'Data Visualization', 'Data Warehouse', 'Database Design',
    'Design Patterns', 'DevOps', 'DNS', 'Docker', 'ETL', 'Firewalls',
    'FOR EMPLOYERS', 'GCP', 'Git', 'GitHub', 'Go', 'Google Analytics',
    'Graphic design', 'HTML', 'Illustrator', 'InDesign', 'Java', 'JavaScript',
    'Jenkins', 'Jira', 'Kanban', 'Kubernetes', 'Linux', 'Machine Learning',
    'Microservices', 'MongoDB', 'MS Project', 'MySQL', 'Network Switches',
    'Node.js', 'NoSQL', 'OO', 'Photoshop', 'PHP', 'Pivot Tables', 'Power BI',
    'PowerShell', 'PRINCE2', 'Python', 'R', 'React', 'RESTful APIs', 'Revit',
    'SaaS', 'Salesforce', 'SAP', 'Scripting Language', 'Scrum', 'SEO',
    'SharePoint', 'SOLID', 'SQL Server', 'Tableau', 'TDD', 'Terraform',
    'TypeScript', 'UI', 'Unit Testing', 'Unix', 'UX', 'Version Control',
    'Virtualization', 'VMware', 'Vue.js', 'Web Services'
]

'''
# Hooked On Recruiting
'''

columns = st.columns(3)
email = columns[0].text_input("Email", value="")

full_name = columns[1].text_input("Full name", value="")

country = columns[2].text_input("Country", value="")

'''### Current Role'''
columns1 = st.columns(2)
title1 = columns1[0].text_input('Job Title')
date1 = columns1[1].date_input("Start Date",
                               datetime.today(), max_value = max_date )
date1 = date1.strftime('%Y-%m-%d %H:%m:%S')

skills1 = st.multiselect('Choose your Top 3 skills',skill_list)

def skillsparse(value,i):
    try:
        return value[i]
    except:
        return f"Please choose skill #{i+1} above to rate"

'''###### Rate your skills'''
columnsSkills = st.columns(3)

help_text = ('''Rating Descriptions:
- *1-Beginner I need lots of help*
- *2-Moderate (I need some guidance)*
- *3-Intermediate (I am independent)*
- *4-Advanced (I have used this skill independently for +1 year)*
- *5-Expert (I can teach others about this skill*''')


skill_1 = columnsSkills[0].slider(f'{skillsparse(skills1,0)}', 1, 5, 3,help=help_text)
skill_2 = columnsSkills[1].slider(f'{skillsparse(skills1,1)}',
                                  1,
                                  5,
                                  3,
                                  help=help_text)
skill_3 = columnsSkills[2].slider(f'{skillsparse(skills1,2)}',
                                  1,
                                  5,
                                  3,
                                  help=help_text)

txt1 = st.text_area('What were your main responsibilities and accomplishments in this role?')

demographics = {"email": email,
                'name': full_name,
                'country':country
}


@st.cache
def save_data():
    currentjob = {
        "jobtitle1":
        title1,
        "startdate1":
        date1,
        'skills1_job_1': (skills1[0], skill_1),
        'skills2_job_1':(skills1[1], skill_2),
        'skills3_job_1':(skills1[2], skill_3),
        'job_desc_1': txt1
    }
    return currentjob

def click_validation():
    if len(skills1)<3:
        return st.error("please choose 3 skills")
    else:
        return save_data()

button1 = st.button('Click to save')

if button1 and "@" not in email:
    st.error("please enter a valid email")
elif button1 and len(skills1) < 3:
    st.error("please choose 3 skills")
elif button1 and len(txt1)<100:
    st.error(f"{len(txt1)} characters. Please fill out minimum 100 characters for your experience")
elif button1 and len(skills1) >= 3:
    currentjob = click_validation()
    st.success("data saved!")
    """# TESTING
    should have all datapoints in JSON"""
    #json.dumps(currentjob,indent=4)
    currentjob
else:
    st.info('Click here to save your info')

#writing skills to a df
#st.write(pd.DataFrame(currentjob.get('skills_job_1'),columns=['skills', 'rating']))
