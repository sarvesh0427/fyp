import streamlit as st
print("Streamlit version:", st.__version__)
print("Attributes:", dir(st))
print("Has experimental_rerun:", hasattr(st, "experimental_rerun"))
