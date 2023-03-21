import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import re

# DO_NOT_CHANGE########################################################
#######################################################################

st.set_page_config(
    page_title='NIQ APP | Maps',
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

image = Image.open('images_main/NIQ_banner.png')

st.image(image, use_column_width='always', output_format='PNG')

if selected == 'Home':
    switch_page('NIQ prototype')

if selected == 'Sampling':
    switch_page('Sampling')

if selected == 'Feasibilities':
    switch_page('Feasibilities')

if selected == 'Maps':
    switch_page('Maps')

if selected == 'More':
    st.write('List of more available subapps.')
    # PANDAS DATABASE CREATION
    # st.set_page_config(
    #    page_title="Sales Dashboard",
    #    page_icon=":bar_chart:",
    #    layout="wide"
    # )

    @st.cache
    def get_data_from_excel():
        df = pd.read_excel(
            io='supermarkt_sales.xlsx',
            engine='openpyxl',
            sheet_name='Sales',
            skiprows=3,
            usecols='B:R',
            nrows=1000,
        )
        # Add 'hour' column to dataframe for second barchart
        df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
        return df

    df = get_data_from_excel()

    # SIDEBAR
    st.sidebar.header("Please Filter Here:")

    city = st.sidebar.multiselect(
        "Select the City:",
        options=df["City"].unique(),
        default=df["City"].unique()
    )

    customer_type = st.sidebar.multiselect(
        "Select the Customer Type:",
        options=df["Customer_type"].unique(),
        default=df["Customer_type"].unique()
    )

    gender = st.sidebar.multiselect(
        "Select the Gender:",
        options=df["Gender"].unique(),
        default=df["Gender"].unique()
    )

    df_selection = df.query(
        "City== @city & Customer_type== @customer_type & Gender == @gender"
    )

    st.dataframe(df_selection)

    # MAINPAGE
    st.title(":bar_chart: Sales Dashboard")
    st.markdown("##")

    # TOP KPI's
    total_sales = int(df_selection["Total"].sum())
    average_rating = round(df_selection["Rating"].mean(), 1)
    star_rating = ":star:" * int(round(average_rating, 0))
    average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

    # KPI's COLUMNS
    left_column, middle_column, right_column = st.columns(3)

    with left_column:
        st.subheader("Total Sales:")
        st.markdown(f"US $ {total_sales:,}")
    with middle_column:
        st.subheader("Average Rating:")
        st.markdown(f"{average_rating} {star_rating}")
    with right_column:
        st.subheader("Average Sales Per Transaction:")
        st.markdown(f"US $ {average_sale_by_transaction}")

    st.markdown("---")

    # BARCHARTS

    # SALES BY PRODUCT LINE [BAR CHART]

    sales_by_product_line = (
        df_selection.groupby(by=["Product line"]).sum()[
            ["Total"]].sort_values(by="Total")
    )

    fig_product_sales = px.bar(
        sales_by_product_line,
        x="Total",
        y=sales_by_product_line.index,
        orientation="h",
        title="<b>Sales by Product Line</b>",
        color_discrete_sequence=["#f05e19"] * len(sales_by_product_line),
        template="plotly_white",
    )

    fig_product_sales.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    df = get_data_from_excel()

    # SALES BY HOUR [BAR CHART]

    sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]

    fig_hourly_sales = px.bar(
        sales_by_hour,
        x=sales_by_hour.index,
        y="Total",
        title="<b>Sales by Hour</b>",
        color_discrete_sequence=["#a2a8f2"] * len(sales_by_hour),
        template="plotly_white",
    )

    fig_hourly_sales.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )

    # Displaying charts
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_product_sales, use_container_width=True)
    right_column.plotly_chart(fig_hourly_sales, use_container_width=True)

    # HIDE STREAMLIT STYLE
    hide_st_style = """
                <style>
                #MainMenu {visibility:hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """

    st.markdown(hide_st_style, unsafe_allow_html=True)


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
