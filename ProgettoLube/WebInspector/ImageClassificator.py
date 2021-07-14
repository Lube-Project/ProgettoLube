import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

import pathlib


class ImageClassificator:
    batch_size = 32
    img_height = 180
    img_width = 180
    class_names = ''
    model = None

    def create_model(self, flag):
        dataset_url = "C:\\Users\\matti\\OneDrive\\Desktop\\logos"

        data_dir = pathlib.Path(dataset_url)

        image_count = len(list(data_dir.glob('*/*.png')))
        print(image_count)

        train_ds = tf.keras.preprocessing.image_dataset_from_directory(
            data_dir,
            validation_split=0.2,
            subset="training",
            seed=123,
            image_size=(self.img_height, self.img_width),
            batch_size=self.batch_size)

        val_ds = tf.keras.preprocessing.image_dataset_from_directory(
            data_dir,
            validation_split=0.2,
            subset="validation",
            seed=123,
            image_size=(self.img_height, self.img_width),
            batch_size=self.batch_size)

        self.class_names = train_ds.class_names
        print(self.class_names)

        AUTOTUNE = tf.data.experimental.AUTOTUNE

        train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
        val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

        normalization_layer = layers.experimental.preprocessing.Rescaling(1. / 255)

        normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
        image_batch, labels_batch = next(iter(normalized_ds))
        first_image = image_batch[0]
        # Notice the pixels values are now in `[0,1]`.
        print(np.min(first_image), np.max(first_image))

        # MODELLO
        data_augmentation = keras.Sequential(
            [
                layers.experimental.preprocessing.RandomFlip("horizontal",
                                                             input_shape=(self.img_height,
                                                                          self.img_width,
                                                                          3)),
                layers.experimental.preprocessing.RandomRotation(0.1),
                layers.experimental.preprocessing.RandomZoom(0.1),
            ]
        )

        # MODIFICARE IN BASE A QUANTE CLASSI SI HANNO
        num_classes = 11

        self.model = Sequential([
            data_augmentation,
            layers.experimental.preprocessing.Rescaling(1. / 255),
            layers.Conv2D(16, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(32, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Dropout(0.2),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(num_classes)
        ])

        self.model.compile(optimizer='adam',
                           loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                           metrics=['accuracy'])

        self.model.summary()

        epochs = 40
        history = self.model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs
        )
        if flag:
            acc = history.history['accuracy']
            val_acc = history.history['val_accuracy']

            loss = history.history['loss']
            val_loss = history.history['val_loss']

            epochs_range = range(epochs)

            plt.figure(figsize=(8, 8))
            plt.subplot(1, 2, 1)
            plt.plot(epochs_range, acc, label='Training Accuracy')
            plt.plot(epochs_range, val_acc, label='Validation Accuracy')
            plt.legend(loc='lower right')
            plt.title('Training and Validation Accuracy')

            plt.subplot(1, 2, 2)
            plt.plot(epochs_range, loss, label='Training Loss')
            plt.plot(epochs_range, val_loss, label='Validation Loss')
            plt.legend(loc='upper right')
            plt.title('Training and Validation Loss')
            plt.show()

    def predict(self, img_path):
        print("CLASSIFICO L'IMMAGINE : " + os.path.basename(img_path))
        try:
            img = keras.preprocessing.image.load_img(
                img_path, target_size=(self.img_height, self.img_width)
            )
        except PIL.UnidentifiedImageError as e:
            print("error on predicting")
            return None

        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)  # Create a batch

        predictions = self.model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        result = os.path.basename(img_path) + " is most likely belongs to {} with a {:.2f} percent confidence.".format(
            self.class_names[np.argmax(score)], 100 * np.max(score))
        print(result)
        return self.class_names[np.argmax(score)]

# sunflower_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/592px-Red_sunflower.jpg"
# sunflower_path = tf.keras.utils.get_file('Red_sunflower', origin=sunflower_url)

# img = keras.preprocessing.image.load_img(
#   'C:\\Users\\matti\\PycharmProjects\\Tensorflow\\logo2.png', target_size=(img_height, img_width)
# )
# img_array = keras.preprocessing.image.img_to_array(img)
# img_array = tf.expand_dims(img_array, 0) # Create a batch

# predictions = model.predict(img_array)
# score = tf.nn.softmax(predictions[0])

# print(
# "This image most likely belongs to {} with a {:.2f} percent confidence."
# .format(class_names[np.argmax(score)], 100 * np.max(score))
# )
