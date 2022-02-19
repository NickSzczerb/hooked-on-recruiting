import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import numpy as np

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

skills1 = st.multiselect('Choose your Top 3 skills',skill_list)

#d = st.date_input("Pick a date", datetime.today(), min_value=min_date)
#new_format = d.strftime('%Y-%m-%d %H:%m:%S')


def skillsparse(value,i):
    try:
        return value[i]
    except:
        return f"Please choose skill #{i+1} above to rate"

'''###### Rate your skills'''
columnsSkills = st.columns(3)

help_text = ('''- *1-Beginner I need lots of help*
- *2-Moderate (I need some guidance)*
- *3-Intermediate (I am independent)*
- *4-Advanced (I have used this skill independently for +1 year)*
- *5-Expert (I can teach others about this skill*''')


skill_1 = columnsSkills[0].slider(f'{skillsparse(skills1,0)}', 1, 5, 2,help=help_text)
skill_2 = columnsSkills[1].slider(f'{skillsparse(skills1,1)}',
                                  1,
                                  5,
                                  2,
                                  help=help_text)
skill_3 = columnsSkills[2].slider(f'{skillsparse(skills1,2)}',
                                  1,
                                  5,
                                  2,
                                  help=help_text)

txt1 = st.text_area('What were your responsibilities and main accomplishments in this role?')
