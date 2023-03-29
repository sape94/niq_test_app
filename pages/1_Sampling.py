import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import re

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
        "nav-link": {"color": "#31333F", "font-size": "15px", "text-align": "centered",
                     "margin": "0px", "--hover-color": "#eee"},
        "nav-link-selected": {"color": "#FFFFFF", "background-color": "#090a47"},
    }
)


@st.cache_data
def cache_df(df, p, conf_lev, s_e):
    c_df = samp_mod.SamplingMachine(sample_portion=p,
                                    confidence_level=conf_lev,
                                    standard_error=s_e).rand_samp(df)
    return c_df


def cache_df_2(df, p, conf_lev, s_e):
    df = df.copy()
    df_2 = df.sample(frac=1)
    c_df_2 = samp_mod.SamplingMachine(sample_portion=p,
                                      confidence_level=conf_lev,
                                      standard_error=s_e).rand_samp(df_2)
    return c_df_2


if selected == 'Home':
    switch_page('NIQ prototype')

if selected == 'Sampling':

    st.markdown('The **sample size\' formula** is the following:')
    st.latex(r'n = \frac{NZ^{2}pq}{e^{2}(N-1)+Z^{2}pq};')
    st.markdown('')
    st.write(r'where $n$ is the **sample size**, $N$ the **population size**, $e$ the **standard error**, $Z$ the **Z-score value** wich is dependent of the **confidence level**, $p$ the **sample portion**, and $q=(1-p)$.')
    st.markdown('')

    with st.expander('If you want to upload a Dataframe, expand this section. When you finish you can collapse it again.'):
        st.write(
            'Upload the CSV file that contains the Dataframe with the feasibility information:')
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

    with st.expander(r'Expandand this section if you know the **sample portion** from previous samples.'):
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
                                 'Yes, by parameters method'))
            if samp_ans == 'Yes, with a non-stratified method':

                sampled_df = cache_df(df=o_df, p=p, conf_lev=conf_lev, s_e=s_e)

                coluno, colunos = st.columns(2, gap='medium')

                with coluno:
                    if st.button(':inbox_tray: Press here to re-sample :inbox_tray:'):
                        sampled_df = cache_df_2(
                            df=o_df, p=p, conf_lev=conf_lev, s_e=s_e)

                st.write(sampled_df)
                sampled_df_csv = sampled_df.to_csv(index=False)

                coldoss, coldos = st.columns(2, gap='medium')

                with coldos:
                    st.download_button(label=':floppy_disk: Download Dataframe as CSV :floppy_disk:',
                                       data=sampled_df_csv,
                                       file_name=f'SAMPLED_{file_name_df}.csv',
                                       mime='text/csv')

                remove_ans = st.radio(
                    'Do you want to remove stores from the sampled Dataframe?', ('No', 'Yes'))

                if remove_ans == 'Yes':

                    col5, col6 = st.columns(2, gap='medium')

                    est_col = ['Player', 'Subplayer', 'City', 'State']
                    sort_col = 'ACV'
                    id_rmv = 'SHO_ID'

                    filter_list = st.multiselect(
                        'Select up to three columns by priority to get the structure:', est_col, max_selections=3)

                    original_rows = o_df.index.values.tolist()
                    used_rows = sampled_df.index.values.tolist()
                    unused_rows = [item for item in original_rows
                                   if item not in used_rows]
                    ws_df = o_df.filter(items=unused_rows, axis=0)
                    ws_df = ws_df.sort_values(by='ACV', ascending=False)

                    rmv_ans = st.radio('Provide the stores by SHO_ID that you want to remove:',
                                       ('Do it by selecting items from a list',
                                        'Upload a Dataframe'))
                    if rmv_ans == 'Do it by selecting items from a list':
                        rmv_list = st.multiselect(
                            f'Select the stores that you want to remove by {id_rmv}', sampled_df[[f'{id_rmv}']])

                    if rmv_ans == 'Upload a Dataframe':
                        up_rmv_file = st.file_uploader("Choose a file",
                                                       type=['csv', 'xlsx'],
                                                       key='settings_df'
                                                       )

                        if up_rmv_file is not None:
                            to_rmv_df = pd.read_csv(up_rmv_file)
                            file_name_df = up_rmv_file.name
                            rmv_list = to_rmv_df['SHO_ID'].to_list()
                        else:
                            rmv_list = []

                    n_s_df = repl_mod.DataFrameReplacer(fulldf=o_df,
                                                        fracdf=sampled_df,
                                                        sort_col=sort_col).add_sts(est_col=est_col,
                                                                                   rmv_list=rmv_list,
                                                                                   id_rmv=id_rmv)

                    new_sampled_df_csv = n_s_df.to_csv(index=False)

                    st.write(n_s_df)

                    col7, col8 = st.columns(2, gap='medium')

                    with col8:
                        st.download_button(label=':floppy_disk: Download Dataframe as CSV :floppy_disk:',
                                           data=new_sampled_df_csv,
                                           file_name=f'NEW_SAMPLED_{file_name_df}.csv',
                                           mime='text/csv')

            if samp_ans == 'Yes, with a stratified method':
                st.write(':arrow_forward: This method is to be implemented soon.')

            if samp_ans == 'Yes, by parameters method':
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
