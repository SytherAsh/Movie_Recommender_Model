

import pandas as pd
import pickle
import requests
import streamlit as st

df=pd.read_csv("Final.csv")
API_KEY = '96f7e2a4'


movie_list = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
def ranking(l1,element):
    mov_list=[]
    for i in l1:
        mov_dict={
            'name': i,
            'index':df.loc[df['title'] == i].index[0],
            'element':(list(df.loc[df['title'] == i][element]))
        }
        
        mov_list.append(mov_dict)
        
    mov_list.sort(key=lambda x:x['element'],reverse=True)
    l2=[]
    for i in mov_list:
        l2.append(i['name'])
    return l2
    

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
    Recommended_Movie_poster=[]
    
    for i in m_list:
        Recommended_Movie_poster.append(get_movie_poster(movie_list.iloc[i[0]].title, API_KEY))
        Recommended_Movies.append(movie_list.iloc[i[0]].title)
    return Recommended_Movies , Recommended_Movie_poster


def get_unique_elements(df):
    unique_elements=set()
    unique_elements = [item for sublist in df for item in (sublist if isinstance(sublist, list) else [sublist])]
    return set(unique_elements)   


def filter_movies_by_type(df, input_list,column):
    return df[df[column].apply(lambda x: all(element in x for element in input_list))]


def movie_button(list_of_movies):    
    st.success("Start!")    
    for i in range(len(list_of_movies)):
        button_key = (f"Review{i}")
        if st.button(f"{list_of_movies[i]}", key=button_key):
            st.session_state.movie = list_of_movies[i]
            st. switch_page("pages/Review.py") 
    st.success("Done!")
def short_list(start_date,end_date,genre,Lang,countries):
    filtered_df = df[df['year'].between(start_date, end_date)]
    filtered_genre= filter_movies_by_type(filtered_df, genre,'genres')
    filtered_lang= filter_movies_by_type(filtered_genre, Lang,'original_language')    
    filtered_coun= filter_movies_by_type(filtered_lang, countries,'production_countries')    
    
    # filtered_coun = filtered_lang[filtered_lang['production_countries'].apply(lambda x: any(country in x for country in countries))]
    x=filtered_coun.title
   
    list_of_movies = x.values.tolist()
    movie_button(list_of_movies)
    