import urllib.request
import streamlit as st
from PIL import Image
import string
import random
from convertor import blur_img, convert_to_grayscale, gen_name, highlight_edges, invert_colors, invert_grayscale
import cv2
import numpy as np
from convertor import *

st.title('Imajify')
file_verified = False

file_or_link = st.radio(
    "Upload image...",
    ('Link', 'Upload file'))

file_name = gen_name()

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
    ('Oil Painting','Inverted Grayscale', 'GrayScale', 'Cartoon', 'Sketch', 'Highlight Edges'))
    # 'Oil Painting', 'Blur'

if file_verified:
    if img_type_to == 'GrayScale':
        grayed = convert_to_grayscale(img)
        st.image(grayed, caption='Final Image', use_column_width='always')
    elif img_type_to == 'Inverted Grayscale':
        grayed = convert_to_grayscale(img)
        inverted = invert_grayscale(grayed)
        st.image(inverted, caption='Final Image', use_column_width='always')
    elif img_type_to == 'Sketch':
        grayed = convert_to_grayscale(img)
        inverted = invert_grayscale(grayed)
        blurred = blur_img(inverted)
        final = cv2.divide(grayed, 255 - blurred, scale=256)
        st.image(final, caption='Final Image', use_column_width='always')
    elif img_type_to == 'Highlight Edges':
        edges = highlight_edges(img)
        st.image(edges, caption='Final Image', use_column_width='always')
    elif img_type_to == 'Cartoon':
        edges = highlight_edges(img)
        result = invert_colors(img)
        cartoonImage = cv2.bitwise_and(result,result,mask=edges)
        st.image(cartoonImage , caption='Final Image', use_column_width='always')

