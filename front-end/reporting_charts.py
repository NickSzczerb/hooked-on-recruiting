import streamlit as st
import plotly.express as px
import pandas as pd
from fpdf import FPDF
from tempfile import NamedTemporaryFile



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

    
def save_pdf(fig):
    pdf = FPDF()  # pdf object
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    pdf.set_font("Times", "B", 18)
    pdf.set_xy(10.0, 20)
    pdf.cell(w=75.0, h=5.0, align="L", txt="This is my sample text")
    with NamedTemporaryFile(delete=True, suffix=".png") as tmpfile:
                fig.write_image(tmpfile.name)
                pdf.image(tmpfile.name, 10, 10, 200, 100)

    st.download_button(
        "Save as PDF",
        data=pdf.output(dest='S').encode('latin-1'),
        file_name="Output.pdf")