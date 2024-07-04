import pandas as pd
import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import function as fl
import pickle

# print(pd.__version__)


API_KEY = '96f7e2a4'
df=pd.read_csv("Final.csv")


movie_list = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

def get_movie_poster(movie_name, api_key):
    url = f'http://www.omdbapi.com/?t={movie_name}&apikey={api_key}'
    response = requests.get(url).json()
    poster_url = response.get('Poster')
    return poster_url


def recommend(movie):
    movie_index = movie_list[movie_list['title']== movie].index[0]
    distances=similarity[movie_index]
    m_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    Recommended_Movies=[]
    Recoomended_Movie_poster=[]
    
    for i in m_list:
        Recoomended_Movie_poster.append(get_movie_poster(movie_list.iloc[i[0]].title, API_KEY))
        Recommended_Movies.append(movie_list.iloc[i[0]].title)
    return Recommended_Movies , Recoomended_Movie_poster


# Define CSS for title alignment
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


col = st.columns((2, 2,2,), gap='medium', vertical_alignment='top')


with col[0]:
    # option=st.selectbox('Select a Movie',movie_list['title'].values)
    
    with st.container(border=True,height=150):
       st.write("HI")
            

with col[1]:
    with st.container(border=True,height=300):
                
        year=fl.get_unique_elements(movie_list.year)
        on = st.toggle("Activate Range Selection")
        date=0
        if on:
            st.write(":green[Activated]")
            start_date, end_date = st.select_slider(
                "Select a range of year",
                options=year,
                value=(1916, 2015))
            st.write(f"You selected from  :green[{start_date}]to :green[{end_date}]")
        else:
            date= st.select_slider(
                "Select a Year",
                options=year,
                value=2016)
            st.write(f"You selected from :green[{date}] ")

with col[2]:
        
    genre=st.multiselect(
        'Genre:',
        options=fl.get_unique_elements(movie_list.genres),
        default=['Drama']
        )  

    Lang=st.multiselect(
        'Language:',
        options=fl.get_unique_elements(movie_list.original_language),
        default=['English']
        )  

    Countries=st.multiselect(
        'Countries:',
        options=fl.get_unique_elements(movie_list.production_countries),
        default=['United States of America']
        
        )  


col = st.columns(1)

with col[0]:
    st.markdown('###  :rainbow[Recommended Movies]', unsafe_allow_html=True)
    
    with st.container(border=True,height=400):
        if date ==0:
            fl.short_list(start_date,end_date,genre,Lang,Countries)
        else:
            fl.short_list(date,date,genre,Lang,Countries)
    
          
# if st.button('GO'):
#     st. switch_page("pages/Review.py") 

# st.warning('This is a warning', icon="⚠️")



# st.info('This is a purely informational message', icon="ℹ️")
# st.snow()
