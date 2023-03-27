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
def sampled(df, sample_size):
    df = feas_df.copy()
    s_df = df.sample(n=sample_size)
    return s_df


def sampled_2(df, sample_size):
    df = feas_df.copy()
    df_2 = df.sample(frac=1)
    s_df_2 = df_2.sample(n=sample_size)
    return s_df_2


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
                                         type=['csv','xlsx'],
                                         key='gral_settings_df'
                                         )
        if uploaded_file is not None:
            try:
                feas_df = pd.read_csv(uploaded_file)
            except:
                feas_df = pd.read_excel(uploaded_file)
            file_name_df = uploaded_file.name
            st.write(feas_df)

    st.markdown('')
    
    with st.expander(r'Expandand this section if you know the **sample portion** from previous samples.'):
        p_100 = st.slider(r'Select the sample\'s portion value, $p$, (%):', 0, 100, 50)
        p = p_100 / 100

    col1, col2 = st.columns(2, gap='medium')

    with col1:
        st.write('Select the **confidence level** (%):')
        conf_lev = st.selectbox(
            r'',
            ('99', '98', '95', '90', '80'))
        #    ('1', '2', '5', '10', '20'))
        c_l = (100 - int(conf_lev))/100

    with col2:
        if c_l == 0.01:
            Z = 2.576
            st.write(r'Then, the **Z-score value**, $Z$, is:')
            z_box = st.selectbox(
                r'',
                ('2.576', '2.326', '1.960', '1.645', '1.282', '0.674'), disabled=True)
        if c_l == 0.02:
            Z = 2.326
            st.write(r'Then, the **Z-score value**, $Z$, is:')
            z_box = st.selectbox(
                r'',
                ('2.326', '2.576', '1.960', '1.645', '1.282', '0.674'), disabled=True)
        if c_l == 0.05:
            Z = 1.96
            st.write(r'Then, the **Z-score value**, $Z$, is:')
            z_box = st.selectbox(
                r'',
                ('1.960', '2.326', '1.645', '2.576', '1.282', '0.674'), disabled=True)
        if c_l == 0.1:
            Z = 1.645
            st.write(r'Then, the **Z-score value**, $Z$, is:')
            z_box = st.selectbox(
                r'',
                ('1.645', '2.576', '2.326', '1.960', '1.282', '0.674'), disabled=True)
        if c_l == 0.2:
            Z = 1.282
            st.write(r'Then, the **Z-score value**, $Z$, is:')
            z_box = st.selectbox(
                r'',
                ('1.282', '1.645', '2.576', '1.960', '2.326', '0.674'), disabled=True)

    st.markdown('')
    st.markdown('')

    col3, col4 = st.columns(2, gap='medium')

    with col3:
        st.write(r'Select, $e$, the **standard error**(%):')
        s_e = st.selectbox(
            r'',
            ('1', '2', '5', '10', '20'))
        e = int(s_e)/100

    with col4:
        if uploaded_file is not None:
            st.write(r'The **population size**, $N$, is:')
            N = feas_df.shape[0]
            N_s = str(N)
            z_box = st.selectbox(
                r'',
                (f'{N_s}', '4'), disabled=True)
        else:
            st.write(r'Type the **population size**, $N$:')
            N = st.number_input('', min_value=1)


    st.markdown('')
    st.markdown('')
    
    col_res_1, col_res_2, col_res_3 = st.columns([1,2,1], gap='medium')
    
    with col_res_2:
        #p = 0.5
        q = 1-p
        n = int(N*(Z**2)*p*q/((e**2)*(N-1)+(Z**2)*p*q))
            
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

                sampled_df = sampled(uploaded_file, n)
                
                coluno, colunos = st.columns(2, gap='medium')
                
                with coluno:
                    if st.button(':inbox_tray: Press here to re-sample :inbox_tray:'):
                        sampled_df = sampled_2(uploaded_file, n)
                        
                st.write(sampled_df)
                sampled_df_csv = sampled_df.to_csv(index=False)
                
                coldoss, coldos = st.columns(2, gap='medium')
                
                with coldos:
                    st.download_button(label=':floppy_disk: Download Dataframe as CSV :floppy_disk:',
                                       data=sampled_df_csv,
                                       file_name=f'SAMPLED_{file_name_df}.csv',
                                       mime='text/csv')
                
                remove_ans = st.radio('Do you want to remove stores from the sampled Dataframe?', ('No', 'Yes'))
                
                if remove_ans == 'Yes':
                
                    col5, col6 = st.columns(2, gap='medium')
                    
                    sampled_df_2 = sampled_df[['Player',
                                                'Subplayer', 'City', 'State']]
                    sampled_df_3 = sampled_df[['SHO_ID']]
                    
                    filter_list = st.multiselect(
                        'Select the columns (by priority) to get the structure', sampled_df_2.columns, max_selections=3)

                    original_rows = feas_df.index.values.tolist()
                    used_rows = sampled_df.index.values.tolist()
                    unused_rows = [item for item in original_rows
                                    if item not in used_rows]
                    # ws_df stands for without sample dataframe.
                    ws_df = feas_df.filter(items=unused_rows, axis=0)
                    ws_df = ws_df.sort_values(by='ACV', ascending=False)

                    rmv_ans = st.radio('Provide the stores by SHO_ID that you want to remove:',
                                        ('Do it by selecting items from a list',
                                        'Upload a Dataframe'))
                    if rmv_ans == 'Do it by selecting items from a list':
                        rmv_list = st.multiselect(
                            'Select the stores that you want to remove by SHO ID', sampled_df_3)
                    
                    if rmv_ans == 'Upload a Dataframe':
                        up_rmv_file = st.file_uploader("Choose a file",
                                            type=['csv'],
                                            key='settings_df'
                                            )
                        if up_rmv_file is None:
                            rmv_list = []
                        if up_rmv_file is not None:
                            to_rmv_df = pd.read_csv(up_rmv_file)
                            file_name_df = up_rmv_file.name
                            #st.write(feas_df)
                            #st.write(to_rmv_df['SHO_ID'])
                            rmv_list = to_rmv_df['SHO_ID'].to_list()
                            
                    
                    col_n = list(sampled_df.columns.values)
                    id_rmv = 'SHO_ID'
                    # Removing the selected stores:
                    rmv_s_df = sampled_df.copy()
                    in_s_df = sampled_df.copy()
                    # rmv_s_df stands for removed stores from sampled dataframe.
                    rmv_s_df = rmv_s_df[rmv_s_df[id_rmv].isin(rmv_list)]
                    # in_s_df stands for incomplete new sampled dataframe.
                    in_s_df = in_s_df[~in_s_df[id_rmv].isin(rmv_list)]
                    # Getting rmv_s_df characteristics:
                    # stc_rmv_df stands for structure of removed items from the sampled dataframe.
                    stc_rmv_df = rmv_s_df[filter_list]
                    # stc_dic stands for stc_rmv_df dictionary.
                    stc_dic = stc_rmv_df.to_dict('list')

                    add_df = pd.DataFrame(columns=col_n)
                    l = len(filter_list)

                    for row in range(0, rmv_s_df.shape[0]):
                        temp_df = ws_df.copy()
                        for i in range(l):
                            temp_df = temp_df[temp_df[filter_list[i]]
                                                == stc_dic[filter_list[i]][row]]
                            if temp_df.empty:
                                break
                        if temp_df.empty:
                            ta_df = ws_df.iloc[0]
                        else:
                            ta_df = temp_df.iloc[0]
                        add_df = pd.concat(
                            [add_df, ta_df.to_frame().transpose()])
                    # Concatenating the incomplete new sampled dataframe and the rows to add
                    # from the unused ones preserving the structure of the removed ones into
                    # a new sampled dataframe.
                    n_s_df = pd.concat([in_s_df, add_df])
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

    col7, col8 = st.columns(2, gap='medium')

    with col7:
        with st.expander('Complementary info'):
            st.write(
                r'Please note that the **confidence level** is equal to 100% minus the standard error, $e$.')

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
<p style='font-size: 0.875em;'>Developed by <a style='display: inline; text-align:
left;' href="https://github.com/sape94" target="_blank"><img src="https://i.postimg.cc/vBnHmZfF/innovation-logo.png"
alt="AI" height= "20"/><br>LatAm's Automation & Innovation Team.</br></a></p>
</div>

</div>
"""
st.write(ft, unsafe_allow_html=True)
