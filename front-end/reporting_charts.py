import streamlit as st
import plotly.express as px
import pandas as pd
from fpdf import FPDF
from tempfile import NamedTemporaryFile
import matplotlib.pyplot as plt
import wordcloud
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np


def radar_chart(skills):
    data = {
        'skills': list(skills.keys()),#['C#','PySpark','Html','.Net','Pandas'],
        'ratings' : list(skills.values())#[float(4), float(8.5), float(5), float(7), float(8.5)]
    }
     
    df = pd.DataFrame(data)
    fig = px.line_polar(df, r='ratings', theta='skills', line_close=True)
    # config = dict({"displaylogo": False,
    #     'modeBarButtonsToRemove': ['pan2d','lasso2d']})
    # fig.show(config=config)
    st.write(fig)
    return fig

def applicant_keyword_cloud(applicant_input):
    wordcloud = WordCloud(
                              background_color='white',
                              #stopwords=20,
                              max_font_size=60, 
                              random_state=42
                             ).generate(applicant_input)
    print(wordcloud)
    plt.imshow(wordcloud)
    plt.axis('off')
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

def save_pdf(fig, wordcloud_fig, title_keyword_fig, prob, full_name, country, title1, date1):
    pdf = FPDF()  # pdf object
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    prob=prob.iloc[:3,[1,0,2]]
    prob.iloc[:,1]=prob.iloc[:,1].round(3)
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
    pdf.cell(epw, 0.0, f'{full_name} from {country}', align = 'C')
    pdf.ln(2*pdf.font_size)
    pdf.cell(epw, 0.0, f'{title1} since the {date1}', align = 'C')
    pdf.ln(2*pdf.font_size)
    col_width = epw/12
    # Document title centered, 'B'old, 14 pt
    pdf.set_font('Times','B',14.0) 
    pdf.cell(epw, 0.0, 'Title Prediction', align='C')

    #fpdf.multi_cell(w: float, h: float, txt: str, border = 0, 
                #align: str = 'J', fill: bool = False)

    pdf.set_font('Times','',10.0) 
    pdf.ln(4*pdf.font_size)
    
    for row in data:
        for x,y in enumerate(row):
            # Enter data in colums
            # Notice the use of the function str to coerce any input to the 
            # string type. This is needed
            # since pyFPDF expects a string, not a number.
            if x == 0:
                pdf.cell(col_width*3, pdf.font_size*3, str(y), border=1)
            elif x == 1:
                pdf.cell(col_width, pdf.font_size*3, str(y), border=1)
            else:
                pdf.multi_cell(col_width*8, pdf.font_size, str(y), border=1)

            #pdf.multi_cell(col_width, pdf.font_size, str(datum), border=1)
        pdf.ln(pdf.font_size)  
    # Line break equivalent to 4 lines
    pdf.ln(4*pdf.font_size)
        
    with NamedTemporaryFile(delete=True, suffix=".png") as tmpfile:
                fig.write_image(tmpfile.name)
                pdf.image(tmpfile.name, 5, 105, 110, 80)
    

    with NamedTemporaryFile(delete=True, suffix=".png") as tmpfile:
               wordcloud_fig.savefig(tmpfile.name, dpi=wordcloud_fig.dpi)
               pdf.image(tmpfile.name, 110, 100, 85, 100)

    with NamedTemporaryFile(delete=True, suffix=".png") as tmpfile:
               #title_keyword_fig.savefig(tmpfile.name, dpi=title_keyword_fig.dpi)
               title_keyword_fig.figure.set_size_inches(6.5, 12.5)
               title_keyword_fig.figure.savefig(tmpfile.name)
               pdf.image(tmpfile.name, 50, 180, 110, 110)

    st.download_button(
        "Save as PDF",
        data=pdf.output(dest='S').encode('latin-1'),
        file_name="Output.pdf")





