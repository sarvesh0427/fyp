import streamlit as st
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Mind Mantra",
    page_icon="streamlit/img1.png",
    layout="wide",
    initial_sidebar_state="auto"
)

st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* Sidebar background /
        [data-testid="stSidebar"] {
            background-color: #f0f2f6 !important; / dark green /
        }

        / Custom navigation styles /
        .sidebar-title {
            font-size: 20px;
            font-weight: bold;
            color: white !important;
            margin-bottom: 20px;
        }

        /* Sidebar container */
        [data-testid="stSidebar"] {
            display: flex;
            flex-direction: column;
            gap: 12px;
            padding: 20px 15px;
            border-radius: 0px 10px 10px 0px;
            width: 500px !important;
            max-width: 400px !important;  /* Adjust as needed */
            min-width: 200px !important;  /* Prevent too small */
            flex-shrink: 1 !important;
           }

        .sidebar-link {
            padding: 10px 15px;
            border-radius: 8px;
            font-size: 15px;
            font-weight: 500;
            background-color: #32CD32; / light green /
            color: white !important;
            text-decoration: none !important;
            transition: background-color 0.3s ease, transform 0.2s ease;
            display: flex;
            align-items: center;
        }

        .sidebar-link i {
            margin-right: 10px;
        }

        .sidebar-link:hover {
            background-color: #2a9e2a;  / darker green */
            transform: translateX(4px);
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

# Import your modules
import home
import thome
import confession
import about
import base64
from io import BytesIO

# def image_to_base64(img):
#     buffered = BytesIO()
#     img.save(buffered, format="PNG")
#     return base64.b64encode(buffered.getvalue()).decode()

# Sidebar navigation
image = Image.open(r'C:\DriveD\fyp\streamlit\img1.png')
image = image.resize((120, 120))
buffered = BytesIO()
image.save(buffered, format="PNG")
img_base64 = base64.b64encode(buffered.getvalue()).decode()
st.sidebar.markdown(
    f"""
    <div style='text-align: center; margin-bottom: 10px;'>
        <img src="data:image/png;base64,{img_base64}" width="120"/>
    </div>
    """,
    unsafe_allow_html=True
)

section = st.sidebar.radio("", ["🏠 Home", "📝 Anonymous Confession Wall", "ℹ️ About"])
# import fhome
# Section logic
if section == "🏠 Home":
    home.home_show()
    # fhome.fhome_show()
    # thome.thome_show()
elif section == "📝 Anonymous Confession Wall":
    confession.confess()
elif section == "ℹ️ About":
    about.about_show()

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<p style='text-align: center; color: #666; margin-top: 20px;'>
    © 2025 Final Year Project | School of Engineering, Pokhara University – Nepal
</p>
""", unsafe_allow_html=True)