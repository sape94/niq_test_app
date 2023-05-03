import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
from app_modules import replacing_module as repl_mod

# DO_NOT_CHANGE########################################################
#######################################################################

st.set_page_config(
    page_title='NIQ APP | Number of Stores',
    layout='centered',
    initial_sidebar_state='collapsed'
)

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

image = Image.open('images_main/NIQ_banner.png')

st.image(image, use_column_width='always', output_format='PNG')

selected = option_menu(
    menu_title=None,
    options=['Home', 'Sampling', 'Feasibilities', 'Maps', 'More'],
    icons=['house', 'calculator', 'archive',
           'map', 'info-circle'],
    menu_icon='cast',
    default_index=4,
    orientation='horizontal',
    styles={
        "container": {"padding": "0!important",
                      "background-color": "#fafafa"},
        "icon": {"color": "#31d1ff", "font-size": "15px"},
        "nav-link": {"color": "#31333F", "font-size": "15px", "text-align": "centered",
                     "margin": "0px", "--hover-color": "#eee"},
        "nav-link-selected": {"color": "#FFFFFF", "background-color": "#090a47"},
    }
)


@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io='MO_ABI_SABMILLER.xlsx',
        engine='openpyxl',
        sheet_name='Sheet1',
        skiprows=0,
        usecols='A:O',
        nrows=1000,
    )
    return df

df = get_data_from_excel()


if selected == 'Home':
    switch_page('NIQ prototype')

if selected == 'Sampling':
    switch_page('Sampling')

if selected == 'Feasibilities':
    switch_page('Feasibilities')

if selected == 'Maps':
    switch_page('Maps')

if selected == 'More':
    st.subheader('Number of stores by criteria')
    df = get_data_from_excel()
    df = df.fillna(0)
    df = df[:-1]
    country_list = ['Colombia']
    tipo_list = ['ABI', 'Standard']
    st.write('Select the **country**:')
    country = st.multiselect('Select one option to continue.', country_list, max_selections=1)
    st.write('')
    if country != []:
        st.write('Select the **department**:')
        department = st.multiselect('Select one or more options to continue.', df['CO_DPTO_ENH_NAME\''].unique(), max_selections=None)
        st.write('')
        if department != []:
            st.write('Select the **county**:')
            temp_county = df[df['CO_DPTO_ENH_NAME\''].isin(department)]['CO_MUNICIPIO_I_NAME\''].sort_values().unique()
            county = st.multiselect('Select one or more options to continue.', temp_county, max_selections=None)
            st.write('')
            if county != []:
                st.write('Select the **store type**:')
                kinds_list = df.columns.to_list()
                kinds_list = kinds_list[3:-1]
                kind = st.multiselect('Select one or more options to continue.', kinds_list, max_selections=None)
                st.write('')
                if kind != []:
                    gf = df[(df['CO_DPTO_ENH_NAME\''].isin(department)) & 
                            (df['CO_MUNICIPIO_I_NAME\''].isin(county)) 
                            ] 
                    ff = gf.loc[:, kind].sum()
                    gg = ff.sum()
                    st.write('')
                    st.write('**Number of stores** that meet the criteria above:')
                    st.write(f'{int(gg)}')

        #######################################################################

ft = """
<style>
a:link , a:visited{
color: #808080;  /* theme's text color at 75 percent brightness*/
background-color: transparent;
text-decoration: none;
}
a:hover,  a:active {
color: #0283C3; /* theme's primary color*/
background-color: transparent;
text-decoration: underline;
}
#page-container {
  position: relative;
  min-height: 10vh;
}
footer{
    visibility:hidden;
}
.footer {
position: relative;
left: 0;
top:230px;
bottom: 0;
width: 100%;
background-color: transparent;
color: #BFBFBF; /* theme's text color at 50 percent brightness*/
text-align: left; /* 'left', 'center' or 'right' if you want*/
}
</style>
<div id="page-container">
<div class="footer">
<p style='font-size: 0.875em;'>Developed by <a style='display: inline;
text-align:
left;' href="https://github.com/sape94" target="_blank">
<img src="https://i.postimg.cc/vBnHmZfF/innovation-logo.png"
alt="AI" height= "20"/><br>LatAm's Automation & Innovation Team.
</br></a></p>
</div>
</div>
"""
st.write(ft, unsafe_allow_html=True)
