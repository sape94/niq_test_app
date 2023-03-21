import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import re

# DO_NOT_CHANGE########################################################
#######################################################################

st.set_page_config(
    page_title='NIQ APP | Feasibilities',
    layout='centered',
    initial_sidebar_state='collapsed'
)

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

selected = option_menu(
    menu_title=None,
    options=['Home', 'Sampling', 'Feasibilities', 'Maps', 'More'],
    icons=['house', 'calculator', 'archive',
           'map', 'info-circle'],
    menu_icon='cast',
    default_index=2,
    orientation='horizontal',
    styles={
        "container": {"padding": "0!important",
                      "background-color": "#fafafa"},
        "icon": {"color": "#31d1ff", "font-size": "15px"},
        "nav-link": {"color": "#31333F", "font-size": "15px", "text-align": "centered",
                     "margin": "0px", "--hover-color": "#eee"},
        "nav-link-selected": {"color": "#FFFFFF", "background-color": "#090a47",
                              "font-size": "12px"},
    }
)

image = Image.open('images_main/NIQ_banner.png')

st.image(image, use_column_width='always', output_format='PNG')

if selected == 'Home':
    switch_page('NIQ prototype')

if selected == 'Sampling':
    switch_page('Sampling')

if selected == 'Feasibilities':
    st.write('List of available feasibilities subapps.')

if selected == 'Maps':
    switch_page('Maps')

if selected == 'More':
    switch_page('More')

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
<p style='font-size: 0.875em;'>Developed by <a style='display: inline; text-align:
left;' href="https://github.com/sape94" target="_blank"><img src="https://i.postimg.cc/vBnHmZfF/innovation-logo.png"
alt="AI" height= "20"/><br>LatAm's Automation & Innovation Team </br></a>.</p>
</div>

</div>
"""
st.write(ft, unsafe_allow_html=True)
