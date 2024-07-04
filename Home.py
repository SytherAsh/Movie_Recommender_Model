import streamlit as st

pages = {
    "🏠Home" : [
        st.Page("pages/Suggest.py",title="Suggest", icon="🛒"),
        st.Page("pages/Compare.py",title="Compare", icon="✏️")
    ],
    "📋Task" : [
        st.Page("pages/Details.py",title="Info", icon="ℹ️"),
        st.Page("pages/Search.py",title="Search", icon="🔍"),
        st.Page("pages/Review.py",title="Review", icon="📷"),
    ]
}

pg = st.navigation(pages)

pg.run()