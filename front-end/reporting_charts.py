import streamlit as st
import plotly.express as px
import pandas as pd
from fpdf import FPDF
from tempfile import NamedTemporaryFile
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np


def radar_chart(skills):
    data = {
        'skills': list(skills.keys()),#['C#','PySpark','Html','.Net','Pandas'],
        'ratings' : list(skills.values())#[float(4), float(8.5), float(5), float(7), float(8.5)]
    }
     
    df = pd.DataFrame(data)
    fig = px.line_polar(df, r='ratings', theta='skills', line_close=True)
    fig.update_traces(fill='toself')

    # config = dict({"displaylogo": False,
    #     'modeBarButtonsToRemove': ['pan2d','lasso2d']})
    # fig.show(config=config)
    st.write(fig)
    return fig

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

def save_pdf(fig, wordcloud_fig, title_keyword_fig, prob, full_name, country, title1, date1):
    pdf = FPDF()  # pdf object
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    prob=prob.iloc[:3,[1,0]]
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

    pdf.ln(5*pdf.font_size)
    pdf.set_font('Times','B',12.0) 
    pdf.cell(epw, 0.0, '                        According to you, your')
    pdf.ln(1.25*pdf.font_size)
    pdf.cell(epw, 0.0, '                        five main skills are :')
    pdf.ln(20*pdf.font_size)
    pdf.cell(epw, 0.0, '                        The most salient words used')
    pdf.ln(1.25*pdf.font_size)
    pdf.cell(epw, 0.0, '                        in your descriptions are :')
    pdf.ln(13*pdf.font_size)
    pdf.cell(epw, 0.0, 'According to our analysis,', align = 'C')
    pdf.ln(1.25*pdf.font_size)
    pdf.cell(epw, 0.0, 'here are the jobs for which', align = 'C')
    pdf.ln(1.25*pdf.font_size)
    pdf.cell(epw, 0.0, 'you might be the more suited', align = 'C')

    with NamedTemporaryFile(delete=True, suffix=".png") as tmpfile:
                fig.write_image(tmpfile.name)
                pdf.image(tmpfile.name, 90, 45, 110, 80)

    with NamedTemporaryFile(delete=True, suffix=".png") as tmpfile:
               wordcloud_fig.savefig(tmpfile.name, dpi=wordcloud_fig.dpi)
               pdf.image(tmpfile.name, 105, 115, 85, 100)

    pdf.ln(6*pdf.font_size)

    pdf.set_font("Times", "B", 10.0)
    for row in data:
        for x,y in enumerate(row):
            # Enter data in colums
            # Notice the use of the function str to coerce any input to the 
            # string type. This is needed
            # since pyFPDF expects a string, not a number.
            if x == 0:
                pdf.cell(col_width*3, pdf.font_size*3, str(y), border=1, align = 'C')
            elif x == 1:
                pdf.cell(col_width, pdf.font_size*3, str(y), border=1, align = 'C')
            else:
                pdf.cell(col_width*8, pdf.font_size, str(y), border=1, align = 'C')


    #pdf.multi_cell(col_width, pdf.font_size, str(datum), border=1) 
    # Line break equivalent to 4 lines

    st.download_button(
        "Save as PDF",
        data=pdf.output(dest='S').encode('latin-1'),
        file_name="Your Job Matching Report.pdf")





