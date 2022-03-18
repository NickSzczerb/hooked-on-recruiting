from ctypes import alignment
from unicodedata import name
from matplotlib import rc
import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import numpy as np
import json
from reporting_charts import save_pdf, hard_skills_radar_chart, soft_skills_radar_chart, applicant_keyword_cloud, job_title_keyword
from models.prediction import run_model
#from prediction import run_model
from mergeJobs import merge_proba

max_date = datetime.today()
hard_skill_list = [
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
    'SharePoint', 'SOLID', 'SQL', 'SQL Server', 'Tableau', 'TDD', 'Terraform',
    'TypeScript', 'UI', 'Unit Testing', 'Unix', 'UX', 'Version Control',
    'Virtualization', 'VMware', 'Vue.js', 'Web Services'

]

soft_skill_list = ['Communication','Teamwork', 'Problem-solving','Time management',
                    'Critical thinking', 'Decision-making', 'Organizational', 'Stress management',
                    'Adaptability', 'Conflict management', 'Leadership', 'Creativity',
                    'Resourcefulness', 'Persuasion', 'Openness to criticism'
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

def hardskillsparse(value,i):
    try:
        return value[i]
    except:
        return f"Hard Skill Nº{i+1}"

def softskillsparse(value,i):
    try:
        return value[i]
    except:
        return f"Soft Skill Nº{i+1}"

'''### Rate your tech skills'''

skills1 = st.multiselect('Choose your top 5 tech skills',hard_skill_list)

columnsHardSkills = st.columns(5)

help_text_skills = ('''Rating Descriptions:
- *1-2: Beginner, I need lots of help*
- *3-4: Moderate, I need some guidance*
- *5-6: Intermediate, I am independent*
- *7-8: Advanced, I have used this skill independently for +1 year*
- *9-10: Expert, I can teach others about this skill*''')


hard_skill_rating_1 = columnsHardSkills[0].slider(f'{hardskillsparse(skills1,0)}',
                                1,
                                10,
                                3,
                                help=help_text_skills)
hard_skill_rating_2 = columnsHardSkills[1].slider(f'{hardskillsparse(skills1,1)}',
                                1,
                                10,
                                3,
                                help=help_text_skills)
hard_skill_rating_3 = columnsHardSkills[2].slider(f'{hardskillsparse(skills1,2)}',
                                1,
                                10,
                                3,
                                help=help_text_skills)
hard_skill_rating_4 = columnsHardSkills[3].slider(f'{hardskillsparse(skills1,3)}',
                                1,
                                10,
                                3,
                                help=help_text_skills)
hard_skill_rating_5 = columnsHardSkills[4].slider(f'{hardskillsparse(skills1,4)}',
                                1,
                                10,
                                3,
                                help=help_text_skills)

'''### Rate your soft skills'''

skills2 = st.multiselect('Choose your top 5 soft skills',soft_skill_list)

columnsSoftSkills = st.columns(5)


soft_skill_rating_1 = columnsSoftSkills[0].slider(f'{softskillsparse(skills2,0)}',
                                1,
                                10,
                                3,
                                help=help_text_skills)
soft_skill_rating_2 = columnsSoftSkills[1].slider(f'{softskillsparse(skills2,1)}',
                                1,
                                10,
                                3,
                                help=help_text_skills)
soft_skill_rating_3 = columnsSoftSkills[2].slider(f'{softskillsparse(skills2,2)}',
                                1,
                                10,
                                3,
                                help=help_text_skills)
soft_skill_rating_4 = columnsSoftSkills[3].slider(f'{softskillsparse(skills2,3)}',
                                1,
                                10,
                                3,
                                help=help_text_skills)
soft_skill_rating_5 = columnsSoftSkills[4].slider(f'{softskillsparse(skills2,4)}',
                                1,
                                10,
                                3,
                                help=help_text_skills)

txt_responsibilities = st.text_area('What were your main responsibilities and accomplishments in this role?')

demographics = {"email": email,
                'name': full_name,
                'country': country
}


@st.cache
def save_data():
    currentjob = {
        "job_title": title1,
        "start_date": date1,
        "hard_skills":
         {
            skills1[0]: int(hard_skill_rating_1),
            skills1[1]: int(hard_skill_rating_2),
            skills1[2]: int(hard_skill_rating_3),
            skills1[3]: int(hard_skill_rating_4),
            skills1[4]: int(hard_skill_rating_5),
         },
        "soft_skills":
        {
            skills2[0]: int(soft_skill_rating_1),
            skills2[1]: int(soft_skill_rating_2),
            skills2[2]: int(soft_skill_rating_3),
            skills2[3]: int(soft_skill_rating_4),
            skills2[4]: int(soft_skill_rating_5),
         },
        'job_desc': txt_responsibilities
    }
    return currentjob

def click_validation():
    if len(skills1) < 5:
        return st.error("Please choose 5 tech skills")
    elif len(skills2) < 5:
        return st.error("Please choose 5 soft skills")
    else:
        return save_data()

button_save = st.button('Click to save you data')


if __name__ == '__main__':

    if button_save and "@" not in email:
        st.error("Please enter a valid email")
    elif button_save and len(title1) < 1:
        st.error("Please input your job title")
    elif button_save and len(skills1) < 5:
        st.error("Please choose 5 skills")
    elif button_save and len(skills2) < 5:
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

        #st.write(results)
        #st.write(return_keywords(txt_responsibilities))
        with st.spinner('Generating your predictions...'):
            results = run_model(txt_responsibilities)
            prob = merge_proba(results)
        '''#### Your tech skills'''
        fig1 = hard_skills_radar_chart(currentjob['hard_skills'])
        '''#### Your soft skills'''
        fig2 = soft_skills_radar_chart(currentjob['soft_skills'])
        '''### Your top 5 recommended jobs'''
        full_results = merge_proba(results).reset_index(drop=True)
        st.table(pd.DataFrame({'Job titles':full_results['jobs'],'Prediction Score':(round(full_results['values']*1000,1).astype(int))}))

        wordcloud_fig = applicant_keyword_cloud(txt_responsibilities)
        #save_pdf(fig, wordcloud_fig, title_keyword_fig, currentjob['skills'])
        title_keyword_fig = job_title_keyword(pd.DataFrame(results['keywords']))

        '''### List of keywords from your responsibilities and accomplishments'''
        kw_table = pd.DataFrame(results['keywords']).rename(columns={
            0: 'Keywords',
            1: 'Relevancy Score'
        })
        st.table(
            kw_table.sort_values(by='Relevancy Score',
                                 ascending=False).reset_index(drop=True))

        save_pdf(fig1, fig2, wordcloud_fig, title_keyword_fig, prob, full_name, country, title1, date1)

    else:
        st.info('Click here to save your info')

#writing skills to a df
#st.write(pd.DataFrame(currentjob.get('skills_job_1'),columns=['skills', 'rating']))
