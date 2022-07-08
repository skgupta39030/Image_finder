
import streamlit as st
from PIL import Image
import glob
import cv2
import pytesseract
import json
import time


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


side = st.sidebar
side.markdown(f'<h2 style="color:tomato;font-size:200%;border-radius:2%;">Image Finder</h2>',
              unsafe_allow_html=True)

rad = st.sidebar.radio("", ["Home", "Find Image", "About Application"])
side.markdown(f'<br>', unsafe_allow_html=True)

sideBarImage = Image.open("./img/OCR_image.png")
side.image(sideBarImage, width=280)


if rad == "Home":
    # st.title("Welcome To Image Finder")
    st.markdown(f"<html><body><h1 style='color:tomato;font-size: 250%;font-family: Arial, Helvetica, sans-serif; margin-top:0%'>Welcome To Image Finder</h1></body></html>", unsafe_allow_html=True)
    st.subheader(
        "Image Finder is a Web Application which aims to find the desired image which user search for.")
    st.write("In our day-to-day life we take countless screenshots, but after sometime when we again want that particular screenshot then it becomes very tedious task to find the desired one.")
    st.write("\nWith the help of our web application, we can easily search the desired screenshot by simply typing any word which was present on that image.")

    sideBarImage = Image.open("./img/sidebarImage.png")

    col1, col2, col3 = st.columns([1, 6, 1])
    col1.write("")
    col2.image(sideBarImage, width=400)
    col3.write("")

    st.subheader("Why Image Finder ?")
    st.write("Image Finder is a user friendly Web Application. It also shows user what technologies it is using. Image Finder gets your Screenshots and extracts text from them and lets you search for the desired one in no time.")
    st.write("This application makes our task much easier as we can just write few words and we can get our Image. It can search for any kind of image like posts, articles, screenshots, documents, etc.")


if rad == "Find Image":
    st.markdown(f"<html><body><h1 style='color:tomato;font-size: 250%;font-family: Arial, Helvetica, sans-serif; margin-top:0%'>Find Your Screenshot..</h1></body></html>", unsafe_allow_html=True)
    instructions = """
        Hey There! You are at the Right Place!! 
        """
    st.subheader(instructions)
    getImagesBtn = st.button("Click Here To Get All ScreenShots")

    st.markdown(f"<h3>Search in the text field to get the desired Image.</h3>",
                unsafe_allow_html=True)

    # path = glob.glob("C:\\Users\\ACER\\Desktop\\SSF\\tesseract\\FlaskSSR\\text_images\\*")
    # path = glob.glob(
    #     "C:\\Users\\ACER\\Desktop\\SSF\\tesseract\\FlaskSSR\\text_images\\*")


#  path where all the images will be fetched from.
    path = glob.glob(
        ".\\text_images\\*")

#
    # path = glob.glob(
    #     "C:\\Users\\ACER\\Pictures\\Screenshots\\*")

    local_css("style.css")
    text_input = st.text_input("")
    col1, col2, col3 = st.columns([1, 6, 2])
    search_btn = col1.button("Search")
    col2.write("")

    dic = {}
    if getImagesBtn:  # getImagesBtn  => perform ocr button
        with st.spinner("Please Wait! AI Is Doing The Work..."):
            for file in path:
                img = cv2.imread(file)
                text = pytesseract.image_to_string(img)
                text = text.replace("\n", " ")
                dic[file] = text.lower()

            my_json = json.dumps(dic)
            with open("imageFinder.json", "w") as outfile:
                outfile.write(my_json)
        with st.success("Hurray!! AI has fetch all your Screenshot"):
            time.sleep(2)
        allImages = []
        allText = []
        with open('imageFinder.json', 'r') as openfile:
            json_object = json.load(openfile)  # Reading from json file
            for key, values in json_object.items():
                key = key.replace("\\", "/")
                allImages.append(key)
                allText.append(values)
            col1, col2 = st.columns(2)
            for i in range(0, int(len(allImages)/2)+1):
                showIncolumnOne = Image.open(allImages[i])
                col1.image(showIncolumnOne)
            for j in range(int(len(allImages)/2)+1, len(allImages)):
                showIncolumnOne = Image.open(allImages[j])
                col2.image(showIncolumnOne)
        allImages_count = len(allImages)
        col3.markdown(
            f"<h6 style='padding:7px 10px 7px 10px;border-radius:5px;border:1px solid tomato;font-weight:lighter'>Total Images: {allImages_count}</h6>", unsafe_allow_html=True)
    if search_btn:
        if text_input == "":
            st.error("Text field cannot be empty!!")
        else:
            new_list_to_store_fetched_images = []
            new_list_to_store_fetched_text = []
            with open('imageFinder.json', 'r') as openfile:
                json_object = json.load(openfile)  # Reading from json file
                for key, values in json_object.items():

                    if text_input.lower() in values:
                        key = key.replace("\\", "/")
                        new_list_to_store_fetched_images.append(key)
                        new_list_to_store_fetched_text.append(values)
                        image1 = Image.open(key)

                        col1, col2, col3 = st.columns([1, 6, 1])
                        col1.write("")
                        col2.image(image1)
                        col3.write("")

                if not new_list_to_store_fetched_images:
                    st.warning("Try Different Text!!")


#  -------------- Code snippet for accessing the text and display it to the user  -------------- #
                    # local_css("style.css")
                    # col2.markdown(
                    #     f"""<h6 style='height:230px;overflow-y:scroll;border:2px solid tomato;border-radius:5px;padding:5px'><b>Text</b><br>%s</h6>"""%(values), unsafe_allow_html=True)

#  -------------- Code snippet for accessing the text and display it to the user  -------------- #

if rad == "About Application":
    st.markdown(f"<h1 style='color:tomato;font-size: 250%;font-family: Arial, Helvetica, sans-serif; margin-top:%'>What technologies we have used: </h1>", unsafe_allow_html=True)

    st.subheader("\n1. Optical Character Recognition (OCR)")
    st.write("Optical character recognition (OCR) technology is a business solution for automating data extraction from printed or written text from a scanned document or image file and then converting the text into a machine-readable form to be used for data processing like editing or searching.")
    st.write("\nA common application of OCR technology is the automated conversion of an image based PDF, TIFF or JPG into a text based machine-readable file. OCR-processed digital files, such as receipts, contracts, invoices, financial statements and more")

    st.write("\n\n")
    sideBarImage = Image.open("./img/ocr3.png")

    col1, col2, col3 = st.columns([1, 6, 1])
    col1.write("")
    col2.image(sideBarImage)
    col3.write("")

    st.write("")

    st.subheader("\n2.Open Source Computer Vision Library:Open CV")
    st.write("OpenCV is a huge open-source library for computer vision, machine learning, and image processing. OpenCV supports a wide variety of programming languages like Python, C++, Java, etc. It can process images and videos to identify objects, faces, or even the handwriting of a human. When it is integrated with various libraries, such as Numpy which is a highly optimized library for numerical operations, then the number of weapons increases in your Arsenal i.e whatever operations one can do in Numpy can be combined with OpenCV.")
    st.write("")

    col1, col2, col3 = st.columns([2, 6, 1])
    opencvImage = Image.open("./img/OpenCV.png")
    col1.write("")
    col2.image(opencvImage)
    col3.write("")

    st.write("")
