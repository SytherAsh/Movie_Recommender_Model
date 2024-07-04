import pandas as pd
import streamlit as st
import requests
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

    #!ranking
    st.subheader(":rainbow[Budget]")
    option_ranking = st.multiselect(
        "Select the movies to compare ranking:",
        movie_list['title'].values)
    list = fl.ranking(option_ranking,'budget')
    with st.container(border=True,height=200):
        if len(list)>=3:
            st.write(f'🥇 {list[0]}')
            st.write(f'🥈 {list[1]}')
            st.write(f'🥉 {list[2]}')
        
            with st.popover("Budget($M)"):
                b1=df[df['title']==list[0]].budget.values[0]
                b2=df[df['title']==list[1]].budget.values[0]
                b3=df[df['title']==list[2]].budget.values[0]
            
                
                st.markdown(
                    """
                    <style>
                    .profit-box {
                        border: 2px solid green;
                        border-radius: 3x;
                        padding: 5px;
                        font-size: 20px;  /* Adjust the font size as needed */
                        color: green;     /* Text color */
                        background-color: #fffdf0;  /* Light green background */
                        font-weight: bold;
                        text-align: center;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                            )
                st.markdown(f'<div class="profit-box"> ${b1:,} M</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="profit-box"> ${b2:,} M</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="profit-box"> ${b3:,} M</div>', unsafe_allow_html=True)
                
                
                

        elif len(list)==2:
            st.write(f'🥇 {list[0]}')
            st.write(f'🥈 {list[1]}')

        elif len(list)==1:
            st.write(f'🥇 {list[0]}')
                
        else:
            st.write(f'🥇 ')
            st.write(f'🥈 ')
            st.write(f'🥉 ')
            
              
with col[1]:
    # option=st.selectbox('Select a Movie',movie_list['title'].values)
    
    #!Profit
    st.subheader(":rainbow[Profit]")
    option_ranking = st.multiselect(
        "Select the movies to compare Profit:",
        movie_list['title'].values)
    list = fl.ranking(option_ranking,'Profit')
    with st.container(border=True,height=200):
        if len(list)>=3:
            st.write(f'🥇 {list[0]}')
            st.write(f'🥈 {list[1]}')
            st.write(f'🥉 {list[2]}')
        
            with st.popover("Profit($M)"):
                b1=df[df['title']==list[0]].Profit.values[0]
                b2=df[df['title']==list[1]].Profit.values[0]
                b3=df[df['title']==list[2]].Profit.values[0]
            
                
                st.markdown(
                    """
                    <style>
                    .profit-box {
                        border: 2px solid green;
                        border-radius: 3x;
                        padding: 5px;
                        font-size: 20px;  /* Adjust the font size as needed */
                        color: green;     /* Text color */
                        background-color: #fffdf0;  /* Light green background */
                        font-weight: bold;
                        text-align: center;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                            )
                st.markdown(f'<div class="profit-box"> ${b1:,} M</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="profit-box"> ${b2:,} M</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="profit-box"> ${b3:,} M</div>', unsafe_allow_html=True)
                
                
                

        elif len(list)==2:
            st.write(f'🥇 {list[0]}')
            st.write(f'🥈 {list[1]}')

        elif len(list)==1:
            st.write(f'🥇 {list[0]}')
                
        else:
            st.write(f'🥇 ')
            st.write(f'🥈 ')
            st.write(f'🥉 ')  
                       
              
with col[2]:
    # option=st.selectbox('Select a Movie',movie_list['title'].values)
    
    #!Profit
    st.subheader(":rainbow[Runtime]")
    option_ranking = st.multiselect(
        "Select the movies to compare Runtime:",
        movie_list['title'].values)
    list = fl.ranking(option_ranking,'runtime')
    with st.container(border=True,height=200):
        if len(list)>=3:
            st.write(f'🥇 {list[0]}')
            st.write(f'🥈 {list[1]}')
            st.write(f'🥉 {list[2]}')
        
            with st.popover("Time"):
                b1=df[df['title']==list[0]].runtime.values[0]
                b2=df[df['title']==list[1]].runtime.values[0]
                b3=df[df['title']==list[2]].runtime.values[0]
            
                
                st.markdown(
                    """
                    <style>
                    .profit-box {
                        border: 2px solid green;
                        border-radius: 3x;
                        padding: 5px;
                        font-size: 20px;  /* Adjust the font size as needed */
                        color: green;     /* Text color */
                        background-color: #fffdf0;  /* Light green background */
                        font-weight: bold;
                        text-align: center;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                            )
                st.markdown(f'<div class="profit-box"> {b1:,} Min</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="profit-box"> {b2:,} Min</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="profit-box"> {b3:,} Min</div>', unsafe_allow_html=True)
                
                
                

        elif len(list)==2:
            st.write(f'🥇 {list[0]}')
            st.write(f'🥈 {list[1]}')

        elif len(list)==1:
            st.write(f'🥇 {list[0]}')
                
        else:
            st.write(f'🥇 ')
            st.write(f'🥈 ')
            st.write(f'🥉 ')  
                       
