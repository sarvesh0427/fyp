# import streamlit as st

# # Your existing set_page_config
# st.set_page_config(
#     page_title="Mind Mantra",
#     page_icon="img.png",
#     layout="centered",
#     initial_sidebar_state="expanded"
# )

# # Inject CSS for sidebar green background
# st.markdown(
#     """
#     <style>
#     /* Sidebar background */
#     [data-testid="stSidebar"] {
#         background-color:  #3CB371;   /* dark green */
#     }
#     /* Optional: Sidebar text color for better contrast */
#     [data-testid="stSidebar"] div, 
#     [data-testid="stSidebar"] span {
#         color: white !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # Then import your modules and do your app logic
# import home
# import confession
# import about

# # Sidebar navigation
# st.sidebar.title("Navigation")
# section = st.sidebar.radio("Go to", ["Home","Anonymous Confession Wall","About"])

# if section == 'Home':
#     home.home_show()

# elif section == 'Anonymous Confession Wall':
#     confession.confess()

# elif section == 'About':
#     about.about_show()

# # footer
# st.markdown("---------")
# st.markdown(
#     "<p style='text-align: center;'>© 2025 Final Year Project | School of Engineering, Pokhara University - Nepal</p>",
#     unsafe_allow_html=True
# )
import streamlit as st

# Your existing set_page_config
st.set_page_config(
    page_title="Mind Mantra",
    page_icon="img1.png",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize dark mode in session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Sidebar CSS for positioning toggle top right
st.sidebar.markdown("""
<style>
.css-1d391kg {  /* sidebar container */
    position: relative;
    padding-top: 30px;
}
.top-right-toggle {
    position: absolute;
    top: 10px;
    right: 15px;
}
</style>
""", unsafe_allow_html=True)

# Dark mode toggle checkbox positioned top right in sidebar
with st.sidebar.container():
    st.markdown('<div class="top-right-toggle">', unsafe_allow_html=True)
    toggle = st.checkbox("Dark Mode", value=st.session_state.dark_mode, key="dark_mode_toggle")
    st.markdown('</div>', unsafe_allow_html=True)
    st.session_state.dark_mode = toggle

# Apply theme based on toggle
def set_theme(dark_mode: bool):
    if dark_mode:
        st.markdown("""
        <style>
        body, .css-1d391kg, .css-1v0mbdj, .stApp {
            background-color: #121212;
            color: white;
        }
        [data-testid="stSidebar"] {
            background-color: #222 !important;
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        /* Sidebar background */
        [data-testid="stSidebar"] {
            background-color:  #3CB371;   /* dark green */
            color: white !important;
        }
        /* Optional: Sidebar text color for better contrast */
        [data-testid="stSidebar"] div, 
        [data-testid="stSidebar"] span {
            color: white !important;
        }
        body, .css-1d391kg, .css-1v0mbdj, .stApp {
            background-color: white;
            color: black;
        }
        </style>
        """, unsafe_allow_html=True)

set_theme(st.session_state.dark_mode)

# Then import your modules and do your app logic
import home
import confession
import about

# Sidebar navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Home","Anonymous Confession Wall","About"])

if section == 'Home':
    home.home_show()

elif section == 'Anonymous Confession Wall':
    confession.confess()

elif section == 'About':
    about.about_show()

# footer
st.markdown("---------")
st.markdown(
    "<p style='text-align: center;'>© 2025 Final Year Project | School of Engineering, Pokhara University - Nepal</p>",
    unsafe_allow_html=True
)
