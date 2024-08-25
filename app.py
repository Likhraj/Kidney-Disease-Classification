import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
import io
import time

# Custom CSS for styling
custom_css = """
    <style>
    .main {
        background-color: white;
    }

    h1, h2, h3 {
        background: -webkit-linear-gradient(45deg, #FF6B6B, #FFD93D, #1E90FF, #00FA9A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    p, div, span, a {
        color: black;
    }

    .custom-spinner {
        border: 16px solid #f3f3f3;
        border-radius: 50%;
        border-top: 16px solid blue;
        width: 120px;
        height: 120px;
        animation: spin 2s linear infinite;
        margin: auto;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .spinner-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
    }

    .loading-text {
        font-size: 40px;
        text-align: center;
        margin: 50px;
    }

    /* Styling for the navigation bar */
    .nav-bar {
        background-color: #f8f9fa;
        margin: 20px;
        padding:20px;
        text-align: center;
        border-bottom: 4px solid #9ac6c0;
    }

    .nav-bar a {
    padding:10px;
    text-decoration:none;
    }
.nav-bar a:hover {
      color:black;
    }

    .sidebar .sidebar-content {
        padding: 20px;
        background-color: #f1f1f1;
    }

    .sidebar img {
        display: block;
        margin: 20px auto;
    }

    .sidebar h2 {
        text-align: center;
        margin-bottom: 20px;
    }

    .st-emotion-cache-9ycgxx{
        color:white;
    }
    .st-emotion-cache-7oyrr6{
    color:black;
    }
    .st-emotion-cache-1erivf3{
    padding: 17px 40px;
    border-radius: 10px;
    border: 0;
    background-color:#9ac6c0;
    letter-spacing: 1.5px;
    font-size: 15px;
    transition: all 0.3s ease;
    box-shadow:  black 0px 10px 0px 0px;
    color: hsl(0, 0%, 100%);
    cursor: pointer;
    }
    .st-emotion-cache-1erivf3:hover{
     box-shadow: #ff944d 0px 7px 0px 0px;
    }
    .st-emotion-cache-fm8pe0 > p{
    color:white;
    }
    .st-emotion-cache-15hul6a{
    background:#F07167;
    }
     .st-emotion-cache-15hul6a:hover{color:white;}

     .st-emotion-cache-1gwvy71{background:black;}

    </style>
"""

# Loading CNN Trained Model
model = tf.keras.models.load_model("Kidney_Classification_Model.keras")

# Remove the spinner and loading text after loading
st.markdown(
    "<style>.spinner-container, .loading-text {display: none;}</style>",
    unsafe_allow_html=True,
)

# Define class labels
class_labels = ["Cyst", "Normal", "Stone", "Tumor"]


def classify_image(image):
    # Convert the image to an array
    image = image.resize((224, 224))  # Resize image to match model's input size
    image_array = img_to_array(image)
    image_array = np.expand_dims(image_array, axis=0)
    image_array = preprocess_input(image_array)

    # Predict the class
    predictions = model.predict(image_array)
    predicted_class = class_labels[np.argmax(predictions)]
    confidence = np.max(predictions)
    confidence = confidence * 100
    return predicted_class, confidence


def generate_pdf_report(image, predicted_class, confidence):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Add title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(130, height - 50, "Kidney Disease Classification Report")

    c.setStrokeColorRGB(0, 0, 0)  # Set line color to black
    c.setLineWidth(1)  # Set line width
    c.line(50, height - 60, width - 50, height - 60)  # Draw line

    # Add the uploaded image on the left side
    image_buffer = io.BytesIO()
    image.save(image_buffer, format='JPEG')
    image_buffer.seek(0)
    img = ImageReader(image_buffer)
    c.drawImage(img, 120, height - 380, width=400, height=300)

    # Add classification result and description on the right side
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, height - 440, "Classification Result")

    c.setFont("Helvetica", 12)
    c.drawString(40, height - 460, f"Prediction: {predicted_class}")
    c.drawString(40, height - 480, f"Confidence Level: {confidence:.2f}%")

    # Add a description about the predicted class
    descriptions = {
        "Cyst": "Cysts are fluid-filled sacs that can develop in the kidneys.Harmless but requires monitoring.",
        "Normal": "The kidney appears normal with no signs of cysts, stones, or tumors.",
        "Stone": "Kidney stones are hard deposits of minerals and salts formed inside the kidneys.",
        "Tumor": "A Tumour or Kidney mass, is an abnormal growth in the kidney.",
    }
    c.drawString(40, height - 500, "Description:")
    c.drawString(
        40, height - 520, descriptions.get(predicted_class, "No description available.")
    )
    c.line(40, height - 540, width - 40, height - 540)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, height - 560, "Contact Information:")
    c.setFont("Helvetica", 12)
    c.drawString(40, height - 580, "Email: Healthcare@gmail.com")
    c.drawString(40, height - 600, "Phone: 011-1234567")

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer


# Display custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Navigation bar
st.markdown(
    """
    <div class="nav-bar">
        <a href="#main-page">Home</a>
        <a href="#about">About</a>
        <a href="#contact">Contact</a>
    </div>
    """,
    unsafe_allow_html=True,
)
import base64


def load_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


# Load the image and encode it to base64
image_base64 = load_image("kidney_brief.jpg")
sidebar_html = f"""
    <style>
        .sidebar-image {{
            width: 100%;
            border: 2px solid white;
            border-radius:10% / 50%;;
            box-shadow:0 0 25px 4px red;
        }}
    </style>
    <img src="data:image/jpeg;base64,{image_base64}" class="sidebar-image" alt="Kidney Image">
    <h1>About kidney.....</h1>
    <p style="color:white;">The kidneys are two bean-shaped organs, each about the size of a fist. They are located just below the rib cage, one on each side of your spine. Healthy kidneys filter about a half cup of blood every minute, removing wastes and extra water to make urine. The urine flows from the kidneys to the bladder through two thin tubes of muscle called ureters, one on each side of your bladder. Your bladder stores urine. Your kidneys, ureters, and bladder are part of your urinary tract.</p>
"""

# Display the HTML in the sidebar

# Sidebar with a project symbol and brief info
st.sidebar.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
st.sidebar.markdown(sidebar_html, unsafe_allow_html=True)
st.sidebar.markdown(
    """
      <style>
    <h1>About kidney.....</h1>
    <p style="color:white;">The kidneys are two bean-shaped organs, each about the size of a fist. They are located just below the rib cage, one on each side of your spine.Healthy kidneys filter about a half cup of blood every minute, removing wastes and extra water to make urine. The urine flows from the kidneys to the bladder through two thin tubes of muscle called ureters, one on each side of your bladder. Your bladder stores urine. Your kidneys, ureters, and bladder are part of your urinary tract.</p>
""",
    unsafe_allow_html=True,
)
st.sidebar.markdown("</div>", unsafe_allow_html=True)

# Main page content
st.markdown('<div id="main-page">', unsafe_allow_html=True)
logo_base64 = load_image("title_image.png")  # Replace 'logo.png' with your logo file

# Create HTML string to display the logo and title together
header_html = f"""
    <style>
        .header-container {{
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .header-title {{
            margin-left: 10px;
            font-size: 36px;
            font-weight: bold;
            background: -webkit-linear-gradient(45deg, #FF6B6B, #FFD93D, #1E90FF, #00FA9A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        }}
        .header-logo {{
            height: 60px;  /* Adjust as needed */
        }}
    </style>
    <div class="header-container">
        <img src="data:image/png;base64,{logo_base64}" class="header-logo" alt="Logo">
        <div class="header-title">Kidney Disease Classification</div>
    </div>
    <br>
"""

# Display the HTML in the main area of the app
st.markdown(header_html, unsafe_allow_html=True)
st.write(
    "Upload a kidney CT scan image, and our model will classify it as Normal, Cyst, Tumor, or Stone. Get accurate and quick diagnosis results with just a few clicks."
)
st.markdown("</div>", unsafe_allow_html=True)

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    # Load the image from the uploaded file
    image = Image.open(uploaded_file)

    # Display the uploaded image on the left
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Classify the uploaded image
    predicted_class, confidence = classify_image(image)

    # Display the classification results on the right
    st.write(f"Prediction: {predicted_class}")
    st.write(f"Confidence Level: {confidence:.2f}%")

    # Generate PDF report
    pdf_report = generate_pdf_report(image, predicted_class, confidence)

    # Provide download link for the PDF report
    st.download_button(
        label="Download Report",
        data=pdf_report,
        file_name="Kidney Report.pdf",
        mime="application/pdf",
    )

# About section
st.markdown('<div id="about">', unsafe_allow_html=True)
st.header("About")
st.markdown(
    """
    <div>
    <p>
    Our advanced kidney classification model uses Convolutional Neural Networks (CNN) to analyze CT scan images and detect potential kidney conditions. By simply uploading a CT scan of the kidney, you can receive a quick and accurate classification, identifying whether the image indicates a Tumor, Cyst, Normal condition, or Stone. Our model leverages cutting-edge AI technology to assist in early diagnosis and provide valuable insights into kidney health.
</p>
<p>
How It Works:
<ul>
    <li><strong>Upload:</strong> Submit your kidney CT scan image.</li>
    <li><strong>Analyze:</strong> Our CNN-based model processes the image and classifies the condition.</li>
    <li><strong>Results:</strong> Receive a clear and precise classification of your kidney health.</li>
</ul>
This tool is designed to support both patients and healthcare professionals by offering fast and reliable diagnostic assistance. Your privacy and data security are paramount, and we ensure that all images and results are handled with the highest level of confidentiality.
</p>
    """,
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)
# Contact section
st.markdown('<div id="contact">', unsafe_allow_html=True)
st.header("Contact")
st.write(
    """
      Dr. Ashwini Goel                                               
      Email:  Ashwini_Goel@gmail.com  
      Phone: +91 99999 54321

      Dr. Anil Kumar Saxena  
      Email: AnilKumar_Saxena@gmail.com  
      Phone: +91 88888 96963
    """
)
st.markdown("</div>", unsafe_allow_html=True)
#
# st.markdown("""
#     <style>
#     .footer{
#         background:red;
#         height:400px;
#         width:1000px;
#         }
#     </style>
#     <div class="footer">
#     He
#     </div>
#
# """, unsafe_allow_html=True)
# Footer
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        height:50px;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        text-align: center;
        padding: 10px;
        border-top: 2px solid #9ac6c0;
    }
    .footer a {
        color: #1E90FF;
        text-decoration: none;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    </style>
    <div class="footer">
        <p>© 2024 Kidney Disease Classification App | <a href="https://example.com" target="_blank">Privacy Policy</a> | <a href="https://example.com" target="_blank">Terms of Service</a></p>
    </div>
    """,
    unsafe_allow_html=True,
)
