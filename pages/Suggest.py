import pandas as pd
import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import function as fl # type: ignore
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

st.markdown(
    """
    <style>
    .fixed-title {
        position: fixed;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        background-color: black;
        padding: 10px 20px;
        font-size: 48px;
        z-index: 1000;
    }
    .stApp {
        margin-top: 60px; /* Adjust this value based on the height of your title */
    }
    /* Reset Streamlit's default padding/margin */
    header, footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# # Your app title
st.markdown('<div class="fixed-title">CineMatch 🎬</div>', unsafe_allow_html=True)

#! To make the text appear below the Header and close to the top of the page
# st.markdown(
#     """
#     <style>
#     .title {
#         text-align: center; /* Center align the title */
#         margin-top: -70px; /* Adjust negative margin to reduce space above */
#         padding-top: 20px; /* Add padding to maintain spacing */
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )


st.title(":rainbow[Movie Similar To Selected]")
option=st.selectbox('Select a Movie',movie_list['title'].values)

col = st.columns(1)


with col[0]:

        
    with st.container(border=True):
        name,poster = recommend(option)

        col1,col2,col3,col4,col5= st.columns(5, gap='medium', vertical_alignment='top')

        with col1:
            st.image(poster[0])
            st.write(name[0])

        with col2:
            st.image(poster[1])
            st.write(name[1])
            
        with col3:
            st.image(poster[2])
            st.write(name[2])
            
        with col4:
            st.image(poster[3])
            st.write(name[3])
            
        with col5:
            st.image(poster[4])    
            st.write(name[4])

        
        
