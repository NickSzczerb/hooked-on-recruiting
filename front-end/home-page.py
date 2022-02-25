from ctypes import alignment
from unicodedata import name
from matplotlib import rc
import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import numpy as np
import json
from reporting_charts import save_pdf, radar_chart

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


#st.image('front-end/logo1.png')

'''# Hooked on Recruiting'''

'''### Fill in your details below'''

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


skill_rating_1 = columnsSkills[0].slider(f'{skillsparse(skills1,0)}', 1, 10, 3,help=help_text)
skill_rating_2 = columnsSkills[1].slider(f'{skillsparse(skills1,1)}',
                                  1,
                                  10,
                                  3,
                                  help=help_text)
skill_rating_3 = columnsSkills[2].slider(f'{skillsparse(skills1,2)}',
                                  1,
                                  10,
                                  3,
                                  help=help_text)

txt_responsibilities = st.text_area('What were your main responsibilities and accomplishments in this role?')

demographics = {"email": email,
                'name': full_name,
                'country':country
}


@st.cache
def save_data():
    currentjob = {
        "job_title": title1,
        "start_date":date1,
        "skills":
         {   
            skills1[0]: float(skill_rating_1),
            skills1[1]: float(skill_rating_2),
            skills1[2]: float(skill_rating_3),
         },  
        'job_desc': txt_responsibilities
    }
    return currentjob

def click_validation():
    if len(skills1)<3:
        return st.error("please choose 3 skills")
    else:
        return save_data()

button_save = st.button('Click to save')


if __name__ == '__main__':
    
    if button_save and "@" not in email:
        st.error("please enter a valid email")
    elif button_save and len(title1)<1:
        st.error("please input your job title")
    elif button_save and len(skills1) < 3:
        st.error("please choose 3 skills")
    elif button_save and len(txt_responsibilities)<100:
        st.error(
            f"Please fill out minimum 100 characters for your experience. {len(txt_responsibilities)}/100 characters filled."
        )
    elif button_save and len(skills1) >= 3:
        currentjob = click_validation()
        st.success("data saved!")
        """# TESTING"""
        #json.dumps(currentjob,indent=4)
        '''#### Demographics'''
        demographics
        '''#### Skills'''
        currentjob
        
        fig = radar_chart(currentjob['skills'])
        save_pdf(fig, currentjob['skills'])
    else:
        st.info('Click here to save your info')

#writing skills to a df
#st.write(pd.DataFrame(currentjob.get('skills_job_1'),columns=['skills', 'rating']))
