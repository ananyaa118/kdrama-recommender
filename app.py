import streamlit as st
import pickle
import pandas as pd
import requests

kdramas_dict = pickle.load(open('kdramas_dict.pkl', 'rb'))
kdramas = pd.DataFrame(kdramas_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(kdrama_id):
    response = requests.get('https://api.themoviedb.org/3/tv/{}?api_key=0360ca73a120ba659eb5ae83dbfa92fc&language=en-US'.format(kdrama_id))
    data = response.json()
    if data['poster_path'] != None:
        return "https://www.themoviedb.org/t/p/w1280" + data['poster_path']
    else:
        return "no-poster.jpg"

def recommend(kdrama):
    kdrama_index = kdramas[kdramas['title'] == kdrama].index[0]
    distances = similarity[kdrama_index]
    kdramas_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_kdramas = []
    recommended_kdramas_posters = []
    for i in kdramas_list:
        kdrama_id = kdramas.iloc[i[0]].id
        # fetch movie title & poster from API
        recommended_kdramas.append(kdramas.iloc[i[0]].title)
        recommended_kdramas_posters.append(fetch_poster(kdrama_id))
    return recommended_kdramas, recommended_kdramas_posters


st.title('K-Drama Recommendation System')

option = st.selectbox(
     'Choose a K-drama for which you would like to get recommendations.',
     kdramas['title'].values)

if st.button('Recommend'):
    names, posters = recommend(option)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.write(names[0])
        st.image(posters[0])
    with col2:
        st.write(names[1])
        st.image(posters[1])
    with col3:
        st.write(names[2])
        st.image(posters[2])
    with col4:
        st.write(names[3])
        st.image(posters[3])
    with col5:
        st.write(names[4])
        st.image(posters[4])