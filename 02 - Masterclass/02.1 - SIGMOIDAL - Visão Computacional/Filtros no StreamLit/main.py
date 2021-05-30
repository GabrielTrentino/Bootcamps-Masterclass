import streamlit as st
import numpy as np
import cv2

from PIL import Image, ImageEnhance

OUTPUT_WIDTH = 500

def main():
    st.title("Master Class Visão Computacional")

    opcoes_menu = ['Filtros', 'Sobre']
    escolha = st.sidebar.selectbox('Escolha uma opção', opcoes_menu)

    # imagem inicial:
    our_image = Image.open("empty.jpg")
    image_file = st.file_uploader("Carregue uma foto e aplique um filtro no menu lateral", type=['jpg', 'jpeg', 'png'])
    if escolha == 'Filtros':
        if image_file is not None:
            st.sidebar.title('Barra Lateral')
            our_image = Image.open(image_file)
            st.sidebar.text('Imagem Original')
            st.sidebar.image(our_image, width=150)

            # filtros que podem ser aplicados:
            filtros = st.sidebar.radio('Filtros', ['Original', 'Grayscale', 'Desenho', 'Sépia',
                                                   'Blur', 'Canny', 'Contraste'])

            if filtros == 'Original':
                our_image = Image.open(image_file)

                st.image(our_image, width=OUTPUT_WIDTH)

            elif filtros == 'Grayscale':
                converted_image = np.array(our_image.convert('RGB'))
                gray_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2GRAY)

                st.image(gray_image, width=OUTPUT_WIDTH)

            elif filtros == 'Desenho':
                b_amount = st.sidebar.slider('Kernel (n x n) ', 3, 33, 7, step=2)
                converted_image = np.array(our_image.convert('RGB'))
                gray_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2GRAY)
                inv_gray_image = 255 - gray_image
                blur_image = cv2.GaussianBlur(inv_gray_image, (b_amount, b_amount), 0, 0)
                sketch_image = cv2.divide(gray_image, 255 - blur_image, scale=256)

                st.image(sketch_image, width=OUTPUT_WIDTH)

            elif filtros == 'Sépia':
                converted_image = np.array(our_image.convert('RGB'))
                converted_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2BGR)
                kernel = np.array([[0.272, 0.534, 0.131],
                                   [0.349, 0.686, 0.168],
                                   [0.393, 0.769, 0.189]])
                sepia_image = cv2.filter2D(converted_image, -1, kernel)

                st.image(sepia_image, channels='BGR', width=OUTPUT_WIDTH)

            elif filtros == 'Blur':
                b_amount = st.sidebar.slider('Kernel (n x n) ', 3, 81, 9, step=2)
                converted_image = np.array(our_image.convert('RGB'))
                converted_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2BGR)
                blur_image = cv2.GaussianBlur(converted_image, (b_amount, b_amount), 0, 0)

                st.image(blur_image, channels='BGR', width=OUTPUT_WIDTH)

            elif filtros == 'Canny':
                b_amount = st.sidebar.slider('Kernel (n x n) ', 3, 15, 7, step=2)
                converted_image = np.array(our_image.convert('RGB'))
                converted_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2BGR)
                blur_image = cv2.GaussianBlur(converted_image, (b_amount, b_amount), 0)
                canny = cv2.cv2.Canny(blur_image, 100, 150)

                st.image(canny, width=OUTPUT_WIDTH)

            elif filtros == 'Contraste':
                c_amount = st.sidebar.slider('Contraste', 0.0, 2.0, 1.0)
                enhacer = ImageEnhance.Contrast(our_image)
                contrast_image = enhacer.enhance(c_amount)
                st.image(contrast_image, width=OUTPUT_WIDTH)
    elif escolha == 'Sobre':
        st.subheader("Este é um projeto da Masterclass Introdução à Visão Computacional.")
        st.markdown('''
                    Esse projeto aborda a utilização da biblioteca CV2 e manipulações de imagens.
                    Desenvolvido por Gabriel Trentino Fróes utilizando as vídeos aulas do Carlos Melo.
                    ''')

if __name__ == '__main__':
    main()