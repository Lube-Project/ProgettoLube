import os
import zipfile

import PIL
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers
from tensorflow.keras import Model
from tensorflow.python.keras.applications.vgg16 import decode_predictions
from tensorflow.python.keras.preprocessing.image import load_img
import numpy as np
import matplotlib.pyplot as plt

from ImageClassificator import ImageClassificator
from OCReader import OCReader
from ReportFoto import ReportFoto


class ImageProcessor:
    vgg = None
    cnn = None

    def run(self):
        if self.vgg is None and self.cnn is None:
            self.create_processors()
        dict_result = {}
        categorie = ['book_jacket', 'web_site', 'monitor', 'scoreboard', 'street_sign', 'perfume', 'carton',
                     'digital_clock'
            , 'hair_spray', 'wall_clock']
        pino = "photo_downloaded\\"
        mypath2 = "C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\"
        paths = [os.path.join("photo_downloaded\\", fn) for fn in next(os.walk("photo_downloaded\\"))[2]]
        temp = []
        counter = 0
        counterLubeCreoERRATI = 0
        counterLubeCreoNi = 0
        counterLubeCreoOk = 0
        counterLubeERRATI = 0
        counterLubeNi = 0
        counterLubeOk = 0
        counterCreoERRATI = 0
        counterCreoNi = 0
        counterCreoOk = 0
        counterCompetitos = 0
        counterNotLogo = 0
        for x in paths:
            temp.append("C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\" + x)
        dict_result['foto_trovate'] = len(temp)
        for x in temp:
            try:
                image = load_img(x,
                                 target_size=(224, 224))

            except PIL.UnidentifiedImageError as e:
                print('error')

            # plt.imshow(image)
            # plt.show()

            # im = cv2.resize(cv2.imread(IMAGE_PATH), (224, 224))
            # il metodo predict si attende un tensore N, 224, 224, 3
            # quindi per una sola immagine deve essere 1, 224, 224, 3
            # im = np.expand_dims(im, axis=0)

            # altro modo di procedere
            image = np.array(image)
            try:
                image = np.expand_dims(image, axis=0)
            except ValueError:
                print('error')
            try:
                predictions = self.vgg.predict(image)
            except ValueError:
                print('error')

            label = decode_predictions(predictions, top=5)
            # retrieve the most likely result, e.g. highest probability
            # print(label)
            label = label[0][0]
            # label = label[0][:]
            # print(label)
            # print the classification
            print('%s (%.2f%%)' % (label[1], label[2] * 100))
            for y in categorie:
                if label[1] == y:
                    counter = counter + 1
                    print("LOGO CORRETTO TROVATO ", x)
                    predizione = self.cnn.predict(x)
                    if predizione == 'lube&creo ERRATI':
                        counterLubeCreoERRATI = counterLubeCreoERRATI + 1
                    if predizione == 'lube&creo loghi ok ma proporzioni o abbinamenti NON CORRETTI':
                        counterLubeCreoNi = counterLubeCreoNi + 1
                    if predizione == 'lube&creo TUTTO OK':
                        counterLubeCreoOk = counterLubeCreoOk + 1
                    if predizione == 'creo ERRATI':
                        counterCreoERRATI = counterCreoERRATI + 1
                    if predizione == 'creo loghi ok ma proporzioni o abbinamenti NON CORRETTI':
                        counterCreoNi = counterCreoNi + 1
                    if predizione == 'creo TUTTO OK':
                        counterCreoOk = counterCreoOk + 1
                    if predizione == 'lube loghi ok ma proporzioni o abbinamenti NON CORRETTI':
                        counterLubeNi = counterLubeNi + 1
                    if predizione == 'lubeERRATI':
                        counterLubeERRATI = counterLubeERRATI + 1
                    if predizione == 'lubeTUTTO OK':
                        counterLubeOk = counterLubeOk + 1
                    if predizione == 'NOT LOGO':
                        counterNotLogo = counterNotLogo + 1
                    if predizione == 'competitors':
                        ocr_reader = OCReader
                        flag = ocr_reader.search_for_competitors(path=x)
                        if flag:
                            counterCompetitos = counterCompetitos + 1


        print(counter)
        dict_result['logo_correctness'] = {
            'lube&creo ERRATI': counterLubeCreoERRATI,
            'lube&creo loghi ok ma proporzioni o abbinamenti NON CORRETTI': counterLubeCreoNi,
            'lube&creo TUTTO OK': counterLubeCreoOk,
            'lube ERRATI': counterLubeERRATI,
            'lube loghi ok ma proporzioni o abbinamenti NON CORRETTI': counterLubeNi,
            'lube TUTTO OK': counterLubeOk,
            'creo ERRATI': counterCreoERRATI,
            'creo loghi ok ma proporzioni o abbinamenti NON CORRETTI': counterCreoNi,
            'creo TUTTO OK': counterCreoOk,
            'competitors': counterCompetitos,
            'not logo': counterNotLogo
        }
        return dict_result

    def ocr_scan(self,platform):
        ocr = OCReader()
        dictionary_parole_dentro_immagine = ocr.read_text_two(platform)
        return dictionary_parole_dentro_immagine

    def create_processors(self):
        self.vgg = VGG16(weights='imagenet', include_top=True)
        self.vgg.compile(optimizer=tf.keras.optimizers.RMSprop(lr=0.0001), loss='binary_crossentropy', metrics=['acc'])
        self.cnn = ImageClassificator()
        flag_stampa_trend_training = False  # modificare se si vuole vedere il grafico del trend
        self.cnn.create_model(flag_stampa_trend_training)

    def generate_report_foto(self, platform):
        x = self.run()
        y = self.ocr_scan(platform)
        report_foto = ReportFoto(x, y)
        return report_foto
    # img_height = 180
    # img_width = 180
    # base_dir = "C:\\Users\\matti\\OneDrive\\Desktop\\vgg16_logos"
    #
    # # train_dir = os.path.join(base_dir, 'training')
    # # validation_dir = os.path.join(base_dir, 'validation')
    # #
    # # # Directory with our training cat pictures
    # # #train_cats_dir = os.path.join(train_dir, 'cats')
    # #
    # # # Directory with our training dog pictures
    # # #train_dogs_dir = os.path.join(train_dir, 'dogs')
    # #
    # # # Directory with our validation cat pictures
    # # #validation_cats_dir = os.path.join(validation_dir, 'cats')
    # #
    # # # Directory with our validation dog pictures
    # # #validation_dogs_dir = os.path.join(validation_dir, 'dogs')
    # #
    # # # Add our data-augmentation parameters to ImageDataGenerator
    # # train_datagen = ImageDataGenerator(rescale=1. / 255., rotation_range=40, width_shift_range=0.2,
    # #                                    height_shift_range=0.2, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
    # #
    # # # Note that the validation data should not be augmented!
    # # test_datagen = ImageDataGenerator(rescale=1.0 / 255.)
    # #
    # # # Flow training images in batches of 20 using train_datagen generator
    # # train_generator = train_datagen.flow_from_directory(train_dir, batch_size=20, class_mode='binary',
    # #                                                     target_size=(224, 224))
    # #
    # # # Flow validation images in batches of 20 using test_datagen generator
    # # validation_generator = test_datagen.flow_from_directory(validation_dir, batch_size=20, class_mode='binary',
    # #                                                         target_size=(224, 224))
    #
    # # base_model = VGG16(input_shape=(224, 224, 3),  # Shape of our images
    # # include_top=False,  # Leave out the last fully connected layer
    # # weights='imagenet')
    #
    # # for layer in base_model.layers:
    # # layer.trainable = False
    #
    # # Flatten the output layer to 1 dimension
    # # x = layers.Flatten()(base_model.output)
    #
    # # Add a fully connected layer with 512 hidden units and ReLU activation
    # # x = layers.Dense(512, activation='relu')(x)
    #
    # # Add a dropout rate of 0.5
    # # x = layers.Dropout(0.5)(x)
    #
    # # Add a final sigmoid layer for classification
    # # x = layers.Dense(1, activation='sigmoid')(x)
    #
    # # model = tf.keras.models.Model(base_model.input, x)
    # model = VGG16(weights='imagenet', include_top=True)
    #
    # model.compile(optimizer=tf.keras.optimizers.RMSprop(lr=0.0001), loss='binary_crossentropy', metrics=['acc'])
    #
    # # vgghist = model.fit(train_generator, validation_data=validation_generator, steps_per_epoch=100, epochs=10)
    #
    # # img = keras.preprocessing.image.load_img(
    # #     'C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\logo.png', target_size=(img_height,img_width)
    # # )
    # # img_array = keras.preprocessing.image.img_to_array(img)
    # # img_array = tf.expand_dims(img_array, 0)  # Create a batch
    #
    # ###############################################################################################################
    # dict_result = {}
    # ic = ImageClassificator()
    # flag_stampa_trend_training = False  # modificare se si vuole vedere il grafico del trend
    # ic.create_model(flag_stampa_trend_training)
    # categorie = ['book_jacket', 'web_site', 'monitor', 'scoreboard', 'street_sign', 'perfume', 'carton', 'digital_clock'
    #     , 'hair_spray', 'wall_clock']
    # pino = "photo_downloaded\\"
    # mypath2 = "C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\"
    # paths = [os.path.join("photo_downloaded\\", fn) for fn in next(os.walk("photo_downloaded\\"))[2]]
    # temp = []
    # counter = 0
    # counterErrati = 0
    # counterNi = 0
    # counterOk = 0
    # for x in paths:
    #     temp.append("C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\" + x)
    # dict_result['foto_trovate'] = len(temp)
    # for x in temp:
    #     try:
    #         image = load_img(x,
    #                          target_size=(224, 224))
    #
    #     except PIL.UnidentifiedImageError as e:
    #         print('error')
    #
    #     # plt.imshow(image)
    #     # plt.show()
    #
    #     # im = cv2.resize(cv2.imread(IMAGE_PATH), (224, 224))
    #     # il metodo predict si attende un tensore N, 224, 224, 3
    #     # quindi per una sola immagine deve essere 1, 224, 224, 3
    #     # im = np.expand_dims(im, axis=0)
    #
    #     # altro modo di procedere
    #     image = np.array(image)
    #     try:
    #         image = np.expand_dims(image, axis=0)
    #     except ValueError:
    #         print('error')
    #     try:
    #         predictions = model.predict(image)
    #     except ValueError:
    #         print('error')
    #
    #     label = decode_predictions(predictions, top=5)
    #     # retrieve the most likely result, e.g. highest probability
    #     # print(label)
    #     label = label[0][0]
    #     # label = label[0][:]
    #     # print(label)
    #     # print the classification
    #     print('%s (%.2f%%)' % (label[1], label[2] * 100))
    #     for y in categorie:
    #         if label[1] == y:
    #             counter = counter + 1
    #             print("LOGO CORRETTO TROVATO ", x)
    #             predizione = ic.predict(x)
    #             if predizione == 'lube&creo ERRATI':
    #                 counterErrati = counterErrati + 1
    #             if predizione == 'lube&creo loghi ok ma proporzioni o abbinamenti NON CORRETTI':
    #                 counterNi = counterNi + 1
    #             if predizione == 'lube&creo TUTTO OK':
    #                 counterOk = counterOk + 1
    #
    # print(counter)
    # dict_result['logo'] = {
    #     'lube&creo ERRATI': str(counterErrati),
    #     'lube&creo loghi ok ma proporzioni o abbinamenti NON CORRETTI': str(counterNi),
    #     'lube&creo TUTTO OK': str(counterOk)
    # }
    #
    # ######################################################################################
    #
    # # image2 = load_img('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\logo2.png',
    # #                  target_size=(224, 224))
    # #
    # # plt.imshow(image2)
    # # plt.show()
    # #
    # # # im = cv2.resize(cv2.imread(IMAGE_PATH), (224, 224))
    # # # il metodo predict si attende un tensore N, 224, 224, 3
    # # # quindi per una sola immagine deve essere 1, 224, 224, 3
    # # # im = np.expand_dims(im, axis=0)
    # #
    # # # altro modo di procedere
    # # image2 = np.array(image2)
    # # image2 = np.expand_dims(image2, axis=0)
    # #
    # # predictions = model.predict(image2)
    # # label = decode_predictions(predictions, top=5)
    # # # retrieve the most likely result, e.g. highest probability
    # # print(label)
    # # label = label[0][0]
    # # # label = label[0][:]
    # # # print(label)
    # # # print the classification
    # # print('%s (%.2f%%)' % (label[1], label[2] * 100))
    # #
    # # ######################################################################################
    # #
    # # image3 = load_img('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\cane.jpg',
    # #                   target_size=(224, 224))
    # #
    # # plt.imshow(image3)
    # # plt.show()
    # #
    # # # im = cv2.resize(cv2.imread(IMAGE_PATH), (224, 224))
    # # # il metodo predict si attende un tensore N, 224, 224, 3
    # # # quindi per una sola immagine deve essere 1, 224, 224, 3
    # # # im = np.expand_dims(im, axis=0)
    # #
    # # # altro modo di procedere
    # # image3 = np.array(image3)
    # # image3 = np.expand_dims(image3, axis=0)
    # #
    # # predictions = model.predict(image3)
    # # label = decode_predictions(predictions, top=5)
    # # # retrieve the most likely result, e.g. highest probability
    # # print(label)
    # # label = label[0][0]
    # # # label = label[0][:]
    # # # print(label)
    # # # print the classification
    # # print('%s (%.2f%%)' % (label[1], label[2] * 100))
    # #
    # # ######################################################################################
    # #
    # # image4 = load_img('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\scavolini.png',
    # #                   target_size=(224, 224))
    # #
    # # plt.imshow(image4)
    # # plt.show()
    # #
    # # # im = cv2.resize(cv2.imread(IMAGE_PATH), (224, 224))
    # # # il metodo predict si attende un tensore N, 224, 224, 3
    # # # quindi per una sola immagine deve essere 1, 224, 224, 3
    # # # im = np.expand_dims(im, axis=0)
    # #
    # # # altro modo di procedere
    # # image4 = np.array(image4)
    # # image4 = np.expand_dims(image4, axis=0)
    # #
    # # predictions = model.predict(image4)
    # # label = decode_predictions(predictions, top=5)
    # # # retrieve the most likely result, e.g. highest probability
    # # print(label)
    # # label = label[0][0]
    # # # label = label[0][:]
    # # # print(label)
    # # # print the classification
    # # print('%s (%.2f%%)' % (label[1], label[2] * 100))
    # #
    # # ######################################################################################
    # #
    # # image5 = load_img('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\promo.png',
    # #                   target_size=(224, 224))
    # #
    # # plt.imshow(image5)
    # # plt.show()
    # #
    # # # im = cv2.resize(cv2.imread(IMAGE_PATH), (224, 224))
    # # # il metodo predict si attende un tensore N, 224, 224, 3
    # # # quindi per una sola immagine deve essere 1, 224, 224, 3
    # # # im = np.expand_dims(im, axis=0)
    # #
    # # # altro modo di procedere
    # # image5 = np.array(image5)
    # # image5 = np.expand_dims(image5, axis=0)
    # #
    # # predictions = model.predict(image5)
    # # label = decode_predictions(predictions, top=5)
    # # # retrieve the most likely result, e.g. highest probability
    # # print(label)
    # # label = label[0][0]
    # # # label = label[0][:]
    # # # print(label)
    # # # print the classification
    # # print('%s (%.2f%%)' % (label[1], label[2] * 100))
    # #
    # # ######################################################################################
    # #
    # # image6 = load_img('C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\images\\car.jpg',
    # #                   target_size=(224, 224))
    # #
    # # plt.imshow(image6)
    # # plt.show()
    # #
    # # # im = cv2.resize(cv2.imread(IMAGE_PATH), (224, 224))
    # # # il metodo predict si attende un tensore N, 224, 224, 3
    # # # quindi per una sola immagine deve essere 1, 224, 224, 3
    # # # im = np.expand_dims(im, axis=0)
    # #
    # # # altro modo di procedere
    # # image6 = np.array(image6)
    # # image6 = np.expand_dims(image6, axis=0)
    # #
    # # predictions = model.predict(image6)
    # # label = decode_predictions(predictions, top=5)
    # # # retrieve the most likely result, e.g. highest probability
    # # print(label)
    # # label = label[0][0]
    # # # label = label[0][:]
    # # # print(label)
    # # # print the classification
    # # print('%s (%.2f%%)' % (label[1], label[2] * 100))
