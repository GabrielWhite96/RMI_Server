import streamlit as st
import Pyro4

uri = "PYRO:video.server@localhost:9090"
server = Pyro4.Proxy(uri)

st.title("Video Client")

videos = server.list_videos()
selected_video = st.selectbox("Select a video", videos)

if st.button("Select"):
    st.write(server.select_video(selected_video))

if st.button("Play"):
    st.write(server.control_video("play"))

if st.button("Pause"):
    st.write(server.control_video("pause"))

if st.button("Stop"):
    st.write(server.control_video("stop"))
