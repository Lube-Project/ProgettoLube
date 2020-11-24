import tensorflow as tf

# Read images from file.
img_raw = tf.io.read_file('C:\\Users\\matti\\PycharmProjects\\Tensorflow\\logo.png')
img1 = tf.io.decode_image(
    img_raw, channels=None, dtype=tf.dtypes.uint8, name=None,
    expand_animations=True
)
img1 = tf.image.resize(img1, (224, 224))
img_raw2 = tf.io.read_file('C:\\Users\\matti\\PycharmProjects\\Tensorflow\\logo2.png')
img2 = tf.io.decode_image(
    img_raw2, channels=None, dtype=tf.dtypes.uint8, name=None,
    expand_animations=True
)
img2 = tf.image.resize(img2, (224, 224))

# Compute SSIM over tf.uint8 Tensors.
ssim1 = tf.image.ssim(img1, img2, max_val=255, filter_size=11,
                      filter_sigma=1.5, k1=0.01, k2=0.03)

# Compute SSIM over tf.float32 Tensors.
im1 = tf.image.convert_image_dtype(img1, tf.float32)
im2 = tf.image.convert_image_dtype(img2, tf.float32)
ssim2 = tf.image.ssim(im1, im2, max_val=1.0, filter_size=11,
                      filter_sigma=1.5, k1=0.01, k2=0.03)
# ssim1 and ssim2 both have type tf.float32 and are almost equal.
#tf.compat.v1.disable_eager_execution()
#with tf.compat.v1.Session() as sess:
#    print(ssim1.eval())
print(ssim1.numpy())
compare1 = ssim1.numpy() *100.0
compare2 = ssim2.numpy() *100.0
print(ssim2.numpy())
print("Le immagini sono simili al : "+str(compare1)+" %")
print("Le immagini sono simili al : "+str(compare2)+" %")

print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
tf.test.gpu_device_name()
tf.config.list_physical_devices('GPU')