import streamlit as st
import requests

st.title('Left or Right Selector with Internet Access')

try:
    response = requests.get('https://api.github.com')
    if response.status_code == 200:
        st.success('Internet access confirmed.')
    else:
        st.warning('Failed to access the internet.')
except Exception as e:
    st.error(f'Error: {e}')

if 'left_count' not in st.session_state:
    st.session_state.left_count = 0
if 'right_count' not in st.session_state:
    st.session_state.right_count = 0

if st.button('Left'):
    st.session_state.left_count += 1
    st.write('You selected Left!')
if st.button('Right'):
    st.session_state.right_count += 1
    st.write('You selected Right!')

st.write('Current Results:')
st.write(f'Left: {st.session_state.left_count}')
st.write(f'Right: {st.session_state.right_count}')
