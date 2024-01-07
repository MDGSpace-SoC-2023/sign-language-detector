import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
import tensorflow as tf

# Load your label map and create category index
label_map_path = '/home/ronit/Documents/SOC/sign langauge detector/TFODCourse/Tensorflow/workspace/annotations/label_map.pbtxt'
category_index = label_map_util.create_category_index_from_labelmap(label_map_path)

# Load your TensorFlow SavedModel for object detection
model_path = '/home/ronit/Documents/SOC/sign langauge detector/TFODCourse/Tensorflow/workspace/models/my_ssd_mobnet/export/saved_model'
detect_fn = tf.saved_model.load(model_path)

# Create a Tkinter window
root = tk.Tk()
root.title("Live Sign Language Translation")

# Create a label for displaying the video stream
video_label = tk.Label(root)
video_label.pack()

# Create a label for displaying detected object class name
translation_label = tk.Label(root, text="Translated word: ")
translation_label.pack()

# Placeholder for detected object class name
detected_object = "No object detected"

# Update translation label text with detected class name
def update_translation(class_name):
    translation_label.config(text="Translated word: " + class_name)
    translation_label.after(500, update_translation, class_name)  # Update every 500 milliseconds with detected class name

# Function for performing object detection and updating the GUI
def perform_detection():
    ret, frame = cap.read()
    if ret:
        image_np = np.array(frame)
        
        # Convert frame data type to uint8
        image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        image_np = tf.convert_to_tensor(image_np, dtype=tf.uint8)

        # Preprocess frame for object detection (resize, normalize, etc.)
        input_tensor = tf.expand_dims(image_np, 0)
        detections = detect_fn(input_tensor)
        
        # Process detection results (bounding boxes, classes, scores)
        detected_classes = detections['detection_classes'][0].numpy().astype(np.int32)
        detected_class_names = [category_index[class_id]['name'] for class_id in detected_classes]

        # Update the translation text with the detected class name (first detected object)
        if detected_class_names:
            detected_object = detected_class_names[0]

        # Update translation label text with detected class name
        update_translation(detected_object)

        # Update the video stream label with detections
        image_np_with_detections = np.array(frame)
        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'][0].numpy(),
            detections['detection_classes'][0].numpy().astype(np.int32),
            detections['detection_scores'][0].numpy(),
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=5,
            min_score_thresh=0.5,
            agnostic_mode=False
        )

        # Convert the frame for displaying using Tkinter
        img = cv2.cvtColor(cv2.resize(image_np_with_detections, (800, 600)), cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)

        video_label.img = img
        video_label.configure(image=img)

    video_label.after(10, perform_detection)  # Call the function again after 10ms

# Video capture setup
cap = cv2.VideoCapture(0)  # Adjust camera index as needed

# Start object detection and video stream display
perform_detection()

# Run the GUI application
root.mainloop()

# Release video capture when the GUI is closed
cap.release()
