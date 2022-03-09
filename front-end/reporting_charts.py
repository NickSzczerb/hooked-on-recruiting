import streamlit as st
import plotly.express as px
import pandas as pd
from fpdf import FPDF
from tempfile import NamedTemporaryFile
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator


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
    
def save_pdf(fig, wordcloud_fig, skills):
    pdf = FPDF()  # pdf object
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    data = [list(skills.keys()), list(skills.values())]

    pdf.set_font("Times", "B", 10.0)
    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/4       
    # Document title centered, 'B'old, 14 pt
    pdf.set_font('Times','B',14.0) 
    pdf.cell(epw, 0.0, 'Demographic data', align='C')
    pdf.set_font('Times','',10.0) 
    pdf.ln(2*pdf.font_size)
    
    for row in data:
        for datum in row:
            # Enter data in colums
            # Notice the use of the function str to coerce any input to the 
            # string type. This is needed
            # since pyFPDF expects a string, not a number.
            pdf.cell(col_width, pdf.font_size, str(datum), border=1)
        pdf.ln(pdf.font_size)  
    # Line break equivalent to 4 lines
    pdf.ln(4*pdf.font_size)     
        
    with NamedTemporaryFile(delete=True, suffix=".png") as tmpfile:
                fig.write_image(tmpfile.name)
                pdf.image(tmpfile.name, 0, 40, 120, 90)
    

    with NamedTemporaryFile(delete=True, suffix=".png") as tmpfile:
               wordcloud_fig.savefig(tmpfile.name, dpi=wordcloud_fig.dpi)
               pdf.image(tmpfile.name, 110, 25, 100, 110)

    st.download_button(
        "Save as PDF",
        data=pdf.output(dest='S').encode('latin-1'),
        file_name="Output.pdf")





