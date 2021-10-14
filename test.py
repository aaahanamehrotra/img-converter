import urllib.request
import streamlit as st
from PIL import Image
import string
import random
import cv2
import numpy as np

N = 7

st.title('Imajify')
file_verified = False

file_or_link = st.radio(
    "Upload image...",
    ('Link', 'Upload file'))

st.write(file_or_link)
res = str(''.join(random.choices(string.ascii_uppercase +
                                         string.digits, k=N)))
file_name = f"{res}.png"
if file_or_link == 'Upload file':

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file:
        try:
            with st.spinner('Processing Image'):
                im = Image.open(uploaded_file)
                im.save(file_name)
                file_verified = True
        except IOError:
            st.error("Please upload an image")
elif file_or_link == 'Link':
    uploaded_file = st.text_input('Link', '')
    if uploaded_file:
        
        # st.write(file_name)
        try:
            with st.spinner('Processing Image'):
                urllib.request.urlretrieve(
                    uploaded_file,
                    file_name)
                im = Image.open(file_name)
                file_verified = True
        except IOError:
            st.error("Please upload an image")


if file_verified:
    st.image(im, caption='Raw Image',
        use_column_width='always')
    img = cv2.imread(file_name)

img_type_to = st.radio(
    "Convert Image to ...",
    ('Inverted Grayscale', 'GrayScale', 'Cartoon', 'Oil Painting', 'Sketch', 'Highlight Edges', 'Blur'))

if file_verified:
    if img_type_to == 'GrayScale':
        grayed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        st.image(grayed, caption='Final Image',
        use_column_width='always')
    elif img_type_to == 'Inverted Grayscale':
        grayed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        inverted = cv2.bitwise_not(grayed)
        st.image(inverted, caption='Final Image',
        use_column_width='always')
    elif img_type_to == 'Sketch':
        grayed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        inverted = cv2.bitwise_not(grayed)
        blurred = cv2.GaussianBlur(inverted, (19, 19), sigmaX=0, sigmaY=0)
        final = cv2.divide(grayed, 255 - blurred, scale=256)
        st.image(final, caption='Final Image',
        use_column_width='always')
    elif img_type_to == 'Highlight Edges':
        lineSize=7
        blurValue=7
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        grayBlur=cv2.medianBlur(gray,blurValue)
        edges=cv2.adaptiveThreshold(grayBlur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,lineSize,blurValue)
        st.image(edges, caption='Final Image',
        use_column_width='always')
    elif img_type_to == 'Cartoon':
        # create edges
        lineSize=7
        blurValue=7
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        grayBlur=cv2.medianBlur(gray,blurValue)
        edges=cv2.adaptiveThreshold(grayBlur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,lineSize,blurValue)
        # invert crs
        colors=9
        data=np.float32(img).reshape((-1,3))
        criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,20,0.001)
        ret,label,center=cv2.kmeans(data,colors,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
        center=np.uint8(center)
        result=center[label.flatten()]
        result=result.reshape(img.shape)
        cartoonImage2=cv2.bitwise_and(result,result,mask=edges)
        st.image(cartoonImage2, caption='Final Image',
        use_column_width='always')

