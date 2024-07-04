# 

        
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import pickle
import requests
alt.themes.enable("dark")

API_KEY = '96f7e2a4'

df=pd.read_csv("Final.csv")
movie_list = pickle.load(open('movies.pkl','rb'))



def make_rating_donut(rating):
    if rating < 6:
        chart_color = ['#E74C3C', '#781F16']  # Red shades
    elif rating > 8:
        chart_color = ['#27AE60', '#12783D']  # Green shades
    else:
        chart_color = ['#3498DB', '#1F618D']    # Blue shades

    source = pd.DataFrame({
        "Topic": ['', 'Rating'],
        "% value": [100-rating*10, rating*10]
    })
    source_bg = pd.DataFrame({
        "Topic": ['', 'Rating'],
        "% value": [100, 0]
    })

    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            domain=['Rating', ''],
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)

    text = plot.mark_text(align='center', color=chart_color[0], font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{rating}/10'))
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            domain=['Rating', ''],
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)
    return plot_bg + plot + text




def make_popularity_donut(popularity):
    if popularity < 10:
        chart_color = ['#E74C3C', '#781F16']  # Red shades
    elif popularity >25:
        chart_color = ['#27AE60', '#12783D']  # Green shades
    else:
       chart_color = ['#FFFF00', '#FBBF00']  # Yellow shades
  

    source = pd.DataFrame({
        "Topic": ['', 'popularity'],
        "% value": [100-popularity, popularity]
    })
    source_bg = pd.DataFrame({
        "Topic": ['', popularity],
        "% value": [100, 0]
    })

    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            domain=['Popularity', ''],
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)

    text = plot.mark_text(align='center', color=chart_color[0], font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{popularity} %'))
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            domain=['Popularity', ''],
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)
    return plot_bg + plot + text


def get_movie_poster(movie_name, api_key):
    url = f'http://www.omdbapi.com/?t={movie_name}&apikey={api_key}'
    response = requests.get(url).json()
    poster_url = response.get('Poster')
    return poster_url



#! PAGE STARTS HERE
#todo PAGE STARTS HERE



st.set_page_config(
    page_title="Review",
    page_icon="⛵",
    layout="wide",
    initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
    .title {
        text-align: center; /* Center align the title */
        margin-top: -70px; /* Adjust negative margin to reduce space above */
        padding-top: 20px; /* Add padding to maintain spacing */
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<h1 class="title">CineMatch 🎬</h1>', unsafe_allow_html=True)


movie=st.selectbox('Select a Movie',movie_list['title'].values)

rating = df.loc[df['title']==movie].vote_average.values[0]
popularity =   df.loc[df['title']==movie].popularity.values[0]
profit =   movie_list.loc[movie_list['title']==movie].Profit.values[0]
budget =   movie_list.loc[movie_list['title']==movie].budget.values[0]



col = st.columns((2, 3, 2), gap='medium', vertical_alignment='top')

with col[0]:
    migrations_col = st.columns((1, 1))
    with migrations_col[0]:
        st.markdown("##### :blue[Rating]")
        st.altair_chart(make_rating_donut(rating), use_container_width=True)
            
        st.markdown("##### :orange[Popularity]", unsafe_allow_html=True)
        st.altair_chart(make_popularity_donut(popularity), use_container_width=True) 
             
    with migrations_col[1]:   
        with st.container(height=150,border=False):   
            st.markdown("##### :green[Profit]", unsafe_allow_html=True)
            if profit>0:           
                # st.write(':green[Profit]')
                
                st.markdown(
                    """
                    <style>
                    .profit-box {
                        border: 2px solid green;
                        border-radius: 5px;
                        padding: 10px;
                        font-size: 20px;  /* Adjust the font size as needed */
                        color: green;     /* Text color */
                        background-color: #f0fdf0;  /* Light green background */
                        font-weight: bold;
                        text-align: center;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                            )
                st.markdown(f'<div class="profit-box"> ${profit:,} M</div>', unsafe_allow_html=True)
            else:
                st.markdown("##### :red[Loss]", unsafe_allow_html=True)
                
                st.markdown(
                    """
                    <style>
                    .profit-box {
                        border: 2px solid red;
                        border-radius: 5px;
                        padding: 10px;
                        font-size: 20px;  /* Adjust the font size as needed */
                        color: red;     /* Text color */
                        background-color: ##FFCCCC;  /* Light red    background */
                        font-weight: bold;
                        text-align: center;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                            )
                st.markdown(f'<div class="profit-box"> ${profit:,} M</div>', unsafe_allow_html=True)
        with st.container(height=150,border=False):    
                            
            st.markdown("##### :violet[Budget ]", unsafe_allow_html=True)
            
            st.markdown(
                """
                <style>
                .budget-box {
                    border: 2px solid violet;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 20px;  /* Adjust the font size as needed */
                    color: violet;     /* Text color */
                    background-color: ##E6E6FA;  /* Light green background */
                    font-weight: bold;
                    text-align: center;
                }
                </style>
                """,
                unsafe_allow_html=True
                        )
            st.markdown(f'<div class="budget-box"> ${budget:,} M</div>', unsafe_allow_html=True)
        
             
             

with col[1]:
    migrations_col = st.columns((0.2, 1, 0.2), gap='medium', vertical_alignment='top')
    with migrations_col[1]:
        st.image(get_movie_poster(movie,API_KEY), 
            caption=movie, 
            use_column_width=False,  # Adjust image width to fit column
            width=300,               # Set specific width (optional)
            #height=400,              # Set specific height (optional)
            clamp=True,              # Clamp image size to specified width and height
            channels='RGB',          # Specify color channels ('RGB' or 'RGBA')
            output_format='PNG'            # Image format (PNG, JPEG, etc.)
            )

with col[2]:
    st.markdown('#### Summary')

    with st.expander('⌚Story', expanded=True):
        st.write(df.loc[df['title']==movie].overview.values[0])

    with st.expander('📷About', expanded=True):
        # movie_list.loc[movie_list['title']==movie].cast.values[0]
        crew=movie_list.loc[movie_list['title']==movie].crew.values[0]
        prod_comp=movie_list.loc[movie_list['title']==movie].production_companies.values[0]
        prod_coun=movie_list.loc[movie_list['title']==movie].production_countries.values[0]
        release=movie_list.loc[movie_list['title']==movie].year.values[0]
        
        
        
        st.write('Director: ',crew[0])
        st.write('Cast: ',movie_list.loc[movie_list['title']==movie].cast.values[0][0])
        st.write('Production Company: ',prod_comp[0])
        st.write('Production Countries: ',prod_coun[0])
        st.write('Release Year: ',release   )
        
        
        