import cv2
import numpy as np
import tensorflow as tf

# =================================================
# AUTO FIND LAST CONV LAYER (SAFE)
# =================================================
def get_last_conv_layer(model):
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            return layer.name
    raise ValueError("❌ No Conv2D layer found in model")


# =================================================
# GRADCAM FUNCTION
# =================================================
def gradcam(model, img_array, layer_name=None):
    """
    img_array: (1, 224, 224, 3)
    returns: heatmap (224x224)
    """

    if layer_name is None:
        layer_name = get_last_conv_layer(model)

    # Build grad model
    grad_model = tf.keras.models.Model(
        inputs=model.inputs,
        outputs=[
            model.get_layer(layer_name).output,
            model.output
        ]
    )

    # Gradient calculation
    with tf.GradientTape() as tape:
        tape.watch(img_array)
        conv_outputs, predictions = grad_model(img_array)
        class_index = tf.argmax(predictions[0])
        loss = predictions[:, class_index]

    # Compute gradients
    grads = tape.gradient(loss, conv_outputs)

    # Global average pooling
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # Weight the feature maps
    conv_outputs = conv_outputs[0]
    heatmap = tf.reduce_sum(conv_outputs * pooled_grads, axis=-1)

    # ReLU & normalize
    heatmap = tf.maximum(heatmap, 0)

    max_val = tf.reduce_max(heatmap)
    if max_val == 0:
        return np.zeros((224, 224))

    heatmap /= max_val

    # Resize to input image size
    heatmap = cv2.resize(
        heatmap.numpy(),
        (img_array.shape[2], img_array.shape[1])
    )

    return heatmap
