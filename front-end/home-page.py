from ctypes import alignment
from unicodedata import name
from matplotlib import rc
import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import numpy as np
import json
from reporting_charts import save_pdf, radar_chart, applicant_keyword_cloud, job_title_keyword
from models.prediction import run_model
#from prediction import run_model
from mergeJobs import merge_proba

max_date = datetime.today()
skill_list = [
    '.NET', '.NET Core', 'Active Directory', 'Agile', 'AI', 'Algorithms', 'Android',
    'Angular', 'Ansible', 'APIs', 'AutoCAD', 'Automated Testing', 'AWS',
    'Azure', 'BDD', 'Big Data', 'Business Intelligence', 'C', 'C#', 'C++',
    'CAD', 'CD', 'Cisco', 'Cloud Platforms', 'Code Reviews', 'Communication', 'Confluence',
    'Continuous Integration', 'CRM', 'CSS', 'Data Analysis', 'Data Modeling',
    'Data Visualization', 'Data Warehouse', 'Database Design',
    'Design Patterns', 'DevOps', 'DNS', 'Docker', 'ETL', 'Firewalls',
    'FOR EMPLOYERS', 'GCP', 'Git', 'GitHub', 'Go', 'Google Analytics',
    'Graphic design', 'HTML', 'Illustrator', 'InDesign', 'Java', 'JavaScript',
    'Jenkins', 'Jira', 'Kanban', 'Kubernetes', 'Linux', 'Machine Learning',
    'Microservices', 'MongoDB', 'MS Project', 'MySQL', 'Network Switches',
    'Node.js', 'NoSQL', 'OO', 'Office', 'Photoshop', 'PHP', 'Pivot Tables', 'Power BI',
    'PowerShell', 'PRINCE2', 'Project Management', 'Python', 'R', 'React', 'RESTful APIs', 'Revit',
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
date1 = date1.strftime('%Y-%m-%d')

skills1 = st.multiselect('Choose your Top 5 skills',skill_list)

def skillsparse(value,i):
    try:
        return value[i]
    except:
        return f"     Skill Nº{i+1}"

'''### Rate your skills'''
columnsSkills = st.columns(5)

help_text_skills = ('''Rating Descriptions:
- *1-2: Beginner, I need lots of help*
- *3-4: Moderate, I need some guidance*
- *5-6: Intermediate, I am independent*
- *7-8: Advanced, I have used this skill independently for +1 year*
- *9-10: Expert, I can teach others about this skill*''')


skill_rating_1 = columnsSkills[0].slider(f'{skillsparse(skills1,0)}', 
                                1, 
                                10, 
                                3,
                                help=help_text_skills)
skill_rating_2 = columnsSkills[1].slider(f'{skillsparse(skills1,1)}',
                                1,
                                10,
                                3,
                                help=help_text_skills)
skill_rating_3 = columnsSkills[2].slider(f'{skillsparse(skills1,2)}',
                                1,
                                10,
                                3,
                                help=help_text_skills)
skill_rating_4 = columnsSkills[3].slider(f'{skillsparse(skills1,3)}',
                                1,
                                10,
                                3,
                                help=help_text_skills)
skill_rating_5 = columnsSkills[4].slider(f'{skillsparse(skills1,4)}',
                                1,
                                10,
                                3,
                                help=help_text_skills)

txt_responsibilities = st.text_area('What were your main responsibilities and accomplishments in this role?')

demographics = {"email": email,
                'name': full_name,
                'country':country
}


@st.cache
def save_data():
    currentjob = {
        "job_title": title1,
        "start_date": date1,
        "skills":
         {
            skills1[0]: int(skill_rating_1),
            skills1[1]: int(skill_rating_2),
            skills1[2]: int(skill_rating_3),
            skills1[3]: int(skill_rating_4),
            skills1[4]: int(skill_rating_5),
         },
        'job_desc': txt_responsibilities
    }
    return currentjob

def click_validation():
    if len(skills1) < 5:
        return st.error("Please choose 5 skills")
    else:
        return save_data()

button_save = st.button('Click to save')


if __name__ == '__main__':

    if button_save and "@" not in email:
        st.error("Please enter a valid email")
    elif button_save and len(title1) < 1:
        st.error("Please input your job title")
    elif button_save and len(skills1) < 3:
        st.error("Please choose 5 skills")
    elif button_save and len(txt_responsibilities) < 100:
        st.error(
            f'''Please fill out a description of your experience as a {title1}. Otherwise we can't help you find your dream job ! {len(txt_responsibilities)}/100 characters minimum'''
        )
    elif button_save and len(skills1) >= 3:
        currentjob = click_validation()
        st.success("data saved!")
        # """# TESTING"""
        # #json.dumps(currentjob,indent=4)
        # '''#### Demographics'''
        # demographics
        # '''#### Skills'''
        # currentjob
        '''### Recommendations'''
        results = run_model(txt_responsibilities)
        prob = merge_proba(results)
        #st.write(results)
        #st.write(return_keywords(txt_responsibilities))
        st.write(merge_proba(results))

        fig = radar_chart(currentjob['skills'])

        wordcloud_fig = applicant_keyword_cloud(txt_responsibilities)
        #save_pdf(fig, wordcloud_fig, title_keyword_fig, currentjob['skills'])
        title_keyword_fig = job_title_keyword(pd.DataFrame(results['keywords']))
        
        save_pdf(fig, wordcloud_fig, title_keyword_fig, prob, full_name, country, title1, date1)

        help_text_keywords = ('Use this list to have a glimpse of what you can do, and what the industry needs')

        '''### List of keywords associated with your profile'''
        st.write(pd.DataFrame(results['keywords']))
    else:
        st.info('Click here to save your info')

#writing skills to a df
#st.write(pd.DataFrame(currentjob.get('skills_job_1'),columns=['skills', 'rating']))
