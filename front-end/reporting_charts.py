import streamlit as st
import plotly.express as px
import pandas as pd
from fpdf import FPDF
from tempfile import NamedTemporaryFile
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np


def hard_skills_radar_chart(hard_skills):
    data = {
        'hard_skills': list(hard_skills.keys()),#['C#','PySpark','Html','.Net','Pandas'],
        'ratings' : list(hard_skills.values())#[float(4), float(8.5), float(5), float(7), float(8.5)]
    }

    df = pd.DataFrame(data)
    fig1 = px.line_polar(df, r='ratings',
                        range_r = [0, 10],
                        theta='hard_skills',
                        line_close=True)
    fig1.update_traces(fill='toself')

    # config = dict({"displaylogo": False,
    #     'modeBarButtonsToRemove': ['pan2d','lasso2d']})
    # fig.show(config=config)
    st.write(fig1)
    return fig1

def soft_skills_radar_chart(soft_skills):
    data = {
        'soft_skills': list(soft_skills.keys()),#['Communication','Persuasion','Openness to criticism','Leadership'],
        'ratings' : list(soft_skills.values())#[float(4), float(8.5), float(5), float(7), float(8.5)]
    }

    df = pd.DataFrame(data)
    fig2 = px.line_polar(df, r='ratings',
                            range_r = [0, 10],
                            theta='soft_skills',
                            line_close=True)
    fig2.update_traces(fill='toself')

    # config = dict({"displaylogo": False,
    #     'modeBarButtonsToRemove': ['pan2d','lasso2d']})
    # fig.show(config=config)
    st.write(fig2)
    return fig2

def applicant_keyword_cloud(applicant_input):
    wordcloud = WordCloud(    background_color='white',
                              #stopwords=20,
                              max_font_size=40,
                              random_state=42
                             ).generate(applicant_input)
    print(wordcloud)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()
    fig = plt.figure(1)
    return fig


def job_title_keyword(title_keyword_df):
    title_keyword_df=title_keyword_df.sort_values(by=title_keyword_df.columns[1], ascending=False)
    X = title_keyword_df.columns[0]
    Y = title_keyword_df.columns[1]
    ax = title_keyword_df.plot.bar(x=X, y=Y, rot=45)
    ax = ax.legend(loc='best')
    return ax

def save_pdf(fig1, fig2, wordcloud_fig, title_keyword_fig, prob, full_name, country, title1, date1):
    pdf = FPDF()  # pdf object
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    prob=prob.iloc[:,[1,0]]
    prob.iloc[:,1]=prob.iloc[:,1].round(3)*1000
    data=[]
    for i in range(len(prob.iloc[:,0])):
        data.append(prob.iloc[i].values.tolist())
    print(data)

    pdf.set_font("Times", "B", 10.0)
    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/4
    # Document title centered, 'B'old, 14 pt
    pdf.set_font('Times','B',25.0)
    pdf.cell(epw, 0.0, 'Hooked On Recruiting', align='C')
    pdf.image('front-end/HookedOnRecruitingLogo.png', 10,8,20)
    pdf.ln(2*pdf.font_size)
    pdf.set_font('Times','B',15.0)
    # User informations
    pdf.cell(epw, 0.0, f'{full_name} from {country}', align = 'C')
    pdf.ln(2*pdf.font_size)
    pdf.cell(epw, 0.0, f'{title1} since the {date1}', align = 'C')
    pdf.ln(2*pdf.font_size)
    col_width = epw/12

    #fpdf.multi_cell(w: float, h: float, txt: str, border = 0,
    #align: str = 'J', fill: bool = False)

    pdf.ln(3*pdf.font_size)
    pdf.set_font('Times','B',13.0)
    pdf.cell(epw, 0.0, '                             Your Tech Skills                                                  Your Soft Skills')
    pdf.ln(24.75*pdf.font_size)
    pdf.cell(epw, 0.0, '                        Word cloud containing')
    pdf.ln(1.25*pdf.font_size)
    pdf.cell(epw, 0.0, '                        your most relevant keywords :')
    pdf.ln(10*pdf.font_size)
    pdf.cell(epw, 0.0, 'According to our analysis, here are your', align = 'C')
    pdf.ln(1.25*pdf.font_size)
    pdf.cell(epw, 0.0, 'top 5 recommended job titles', align='C')

    with NamedTemporaryFile(delete=True, suffix=".png") as tmpfile:
        fig1.write_image(tmpfile.name)
        pdf.image(tmpfile.name, 5, 70, 110, 80)

    with NamedTemporaryFile(delete=True, suffix=".png") as tmpfile:
        fig2.write_image(tmpfile.name)
        pdf.image(tmpfile.name, 96, 70, 110, 80)

    with NamedTemporaryFile(delete=True, suffix=".png") as tmpfile:
        wordcloud_fig.savefig(tmpfile.name, dpi=wordcloud_fig.dpi)
        pdf.image(tmpfile.name, 115, 140, 70, 85)

    pdf.ln(3*pdf.font_size)

    pdf.set_font("Times", "B", 12.0)
    for row in data:
        for x,y in enumerate(row):
            # Enter data in colums
            # Notice the use of the function str to coerce any input to the
            # string type. This is needed
            # since pyFPDF expects a string, not a number.
            if x == 0:
                pdf.cell(col_width*3.47, pdf.font_size)
                pdf.cell(col_width*4, pdf.font_size*1.30, str(y), border=1, align = 'C')
            elif x == 1:
                pdf.cell(col_width, pdf.font_size*1.30, str(y), border=1, ln=1, align = 'C')


    #pdf.multi_cell(col_width, pdf.font_size, str(datum), border=1)
    # Line break equivalent to 4 lines

    st.download_button(
        "Generate your PDF",
        data=pdf.output(dest='S').encode('latin-1'),
        file_name="Your Job Matching Report.pdf")
