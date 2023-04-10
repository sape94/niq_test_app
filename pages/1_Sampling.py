import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
from app_modules import sampling_module as samp_mod
from app_modules import replacing_module as repl_mod

# DO_NOT_CHANGE########################################################
#######################################################################

st.set_page_config(
    page_title='NIQ APP | Sampling',
    layout='centered',
    initial_sidebar_state='collapsed'
)

hide_menu_style = """
        <style>
        #MainMenu {visibility: display;}
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
    default_index=1,
    orientation='horizontal',
    styles={
        "container": {"padding": "0!important",
                      "background-color": "#fafafa"},
        "icon": {"color": "#31d1ff", "font-size": "15px"},
        "nav-link": {"color": "#31333F", "font-size": "15px",
                     "text-align": "centered",
                     "margin": "0px", "--hover-color": "#eee"},
        "nav-link-selected": {"color": "#FFFFFF",
                              "background-color": "#090a47"},
    }
)


@st.cache_data
def cache_df(o_df, p, conf_lev, s_e):
    cc_1 = samp_mod.SamplingMachine(sample_portion=p,
                                    confidence_level=conf_lev,
                                    standard_error=s_e).rand_samp(o_df)
    return cc_1


def cache_df_2(o_df, p, conf_lev, s_e):
    cc_2 = samp_mod.SamplingMachine(sample_portion=p,
                                    confidence_level=conf_lev,
                                    standard_error=s_e).rand_samp(o_df)
    return cc_2


if selected == 'Home':
    switch_page('NIQ prototype')

if selected == 'Sampling':
    subhead_app_1 = '''
    <style>
    .subhead-item {
        backgroundcolor: transparent;
    }
    .subhead-item:hover {
        color: #2E6EF7;
    }
    </style>

    <h3 class="subhead-item">
    Sampling app
    </h3>
    '''
    st.write(subhead_app_1, unsafe_allow_html=True)

    st.markdown('The **sample size\' formula** is the following:')
    st.latex(r'n = \frac{NZ^{2}pq}{e^{2}(N-1)+Z^{2}pq};')
    st.markdown('')
    st.write(r'where $n$ is the **sample size**, $N$ the **population size**, $e$ the **standard error**, $Z$ the **Z-score value** wich is dependent of the **confidence level**, $p$ the **sample portion**, and $q=(1-p)$.')
    st.markdown('')

    with st.expander('If you want to upload a Dataframe, expand this section. When you finish you can collapse it again.'):
        st.write(
            'Upload the CSV or XLSX file that contains the working Dataframe:')
        uploaded_file = st.file_uploader("Choose a file",
                                         type=['csv', 'xlsx'],
                                         key='gral_settings_df'
                                         )
        if uploaded_file is not None:
            try:
                o_df = pd.read_csv(uploaded_file, encoding='UTF8')
            except:
                o_df = pd.read_excel(uploaded_file, encoding='UTF8')

            try:
                file_name_df = uploaded_file.name.replace('.csv', '')
            except:
                try:
                    file_name_df = uploaded_file.name.replace('.xlsx', '')
                except:
                    pass
            st.write(o_df)

    st.markdown('')

    with st.expander(r'Expand this section if you know the **sample portion** from previous samples.'):
        p_100 = st.slider(
            r'Select the sample\'s portion value, $p$, (%):', 0, 100, 50)
        p = int(p_100)

    col1, col2 = st.columns(2, gap='medium')

    with col1:
        st.write('Select the **confidence level** (%):')
        conf_lev = st.selectbox(
            r'',
            ('99', '98', '95', '90', '85', '80'))

    with col2:
        z_score_dict = {99: 2.576,
                        98: 2.326,
                        95: 1.96,
                        90: 1.645,
                        85: 1.44,
                        80: 1.282}
        st.write(r'Then, the **Z-score value**, $Z$, is:')
        z_s = str(z_score_dict[int(conf_lev)])
        z_box = st.selectbox(r'',
                             (f'{z_s}', '0'), disabled=True)

    st.markdown('')
    st.markdown('')

    col3, col4 = st.columns(2, gap='medium')

    with col3:
        st.write(r'Select, $e$, the **standard error**(%):')
        s_e = st.selectbox(
            r'',
            ('1', '2', '5', '10', '20'))

    with col4:
        if uploaded_file is not None:
            st.write(r'The **population size**, $N$, is:')
            N = o_df.shape[0]
            N_s = str(N)
            z_box = st.selectbox(
                r'',
                (f'{N_s}', '4'), disabled=True)
        else:
            st.write(r'Type the **population size**, $N$:')
            N = st.number_input('', min_value=1)

    st.markdown('')
    st.markdown('')

    col_res_1, col_res_2, col_res_3 = st.columns([1, 2, 1], gap='medium')

    with col_res_2:
        n = samp_mod.SamplingMachine(sample_portion=p,
                                     confidence_level=conf_lev,
                                     standard_error=s_e).calc_samp(population_size=N)

        st.markdown(
            r':arrow_forward::arrow_forward: Then, the **sample size** is:')
        st.latex(f'n = {n}')

    st.markdown('')
    st.markdown('')

    if uploaded_file is not None:
        with st.expander('If you want to sample the Dataframe, expand this section. When you finish you can collapse it again.'):
            samp_ans = st.radio('Do you want to sample your Dataframe?',
                                ('No',
                                 'Yes, with a non-stratified method',
                                 'Yes, with a stratified method',
                                 'Yes, with a parameters method'))
            if samp_ans == 'Yes, with a non-stratified method':

                # sampled_df = samp_mod.SamplingMachine(sample_portion=p,
                #                                      confidence_level=conf_lev,
                #                                      standard_error=s_e).rand_samp(o_df)
                sampled_df = cache_df(o_df, p=p, conf_lev=conf_lev, s_e=s_e)

                # coluno, colunos = st.columns(2, gap='medium')

                # with coluno:
                if st.button(':inbox_tray: Press here to re-sample :inbox_tray:'):
                    # sampled_df = samp_mod.SamplingMachine(sample_portion=p,
                    #                                      confidence_level=conf_lev,
                    #                                      standard_error=s_e).rand_samp(o_df.sample(frac=1))
                    o_df = o_df.sample(frac=1)
                    sampled_df = cache_df_2(
                        o_df, p=p, conf_lev=conf_lev, s_e=s_e)

                st.write(sampled_df)
                sampled_df_csv = sampled_df.to_csv(index=False)

                coldoss, coldos = st.columns(2, gap='medium')

                with coldos:
                    st.download_button(label=':floppy_disk: Download Dataframe as CSV :floppy_disk:',
                                       data=sampled_df_csv,
                                       file_name=f'SAMPLED_{file_name_df}.csv',
                                       mime='text/csv')

                st.write('')
                st.write('Don\'t forget to **download** your sampled Dataframe.')
                st.write(
                    'If you want to remove stores from the sampled Dataframe use our:')
                subhead_app_2 = '''
                <style>
                .subhead-item_2 {
                    color: #2E6EF7;
                    backgroundcolor: transparent;
                }
                .subhead-item_2:hover {
                    color: #164fc9;
                }
                </style>

                <a style='display: inline; text-align: center; color: #31333F
                ; text-decoration: none; '
                href="/Replacing" target="_self">
                <h5 class="subhead-item_2">
                Replacing app
                </h5>
                </a>
                '''
                st.write(subhead_app_2, unsafe_allow_html=True)
                st.write('')
                st.write('')

            if samp_ans == 'Yes, with a stratified method':
                st.write(':arrow_forward: This method is to be implemented soon.')

            if samp_ans == 'Yes, with a parameters method':
                st.write(':arrow_forward: This method is to be implemented soon.')

    col7, col8 = st.columns([2, 1], gap='medium')

    with col7:
        with st.expander('Complementary info'):
            st.write(r'The **Z-score value**, $Z$, is such that:')
            st.latex(
                r'\int_{Z}^{\infty}\textrm{w}_{\textrm{G}}(\tau)\textrm{d}\tau=\frac{\alpha}{2};')
            st.write('where:')
            st.markdown(
                r'- $\textrm{w}_{\textrm{G}}(\tau)$ is the **normal** probability density function,')
            st.write(r'- $\alpha\in[0,1]$, the **confidence level**.')
            st.write('')


if selected == 'Feasibilities':
    switch_page('Feasibilities')

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

