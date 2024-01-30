import tkinter as tk
import cv2
import os
import numpy as np
from PIL import Image, ImageTk
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
import tensorflow as tf


files = {
    'PIPELINE_CONFIG':os.path.join('Tensorflow', 'workspace','models', 'my_ssd_mobnet', 'pipeline.config'),
}

paths = {
    'CHECKPOINT_PATH': os.path.join('Tensorflow', 'workspace','models','my_ssd_mobnet')
 }
# Load your label map and create category index
label_map_path = '/home/ronit/Documents/SOC/sign langauge detector/TFODCourse/Tensorflow/workspace/annotations/label_map.pbtxt'
category_index = label_map_util.create_category_index_from_labelmap(label_map_path)

def extract_class_names(label_map_path):
    class_names = []
    with open(label_map_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("name:"):
                class_name = line.split("'")[1]
                class_names.append(class_name)
    return class_names

# Extract class names from the label_map.pbtxt file
class_names_list = extract_class_names(label_map_path)

# Print the extracted class names
print(class_names_list)

# Load your TensorFlow SavedModel for object detection
model_path = 'Tensorflow/workspace/models/my_ssd_mobnet/export/saved_model'
detect_fn = tf.saved_model.load(model_path)

# Create a Tkinter window
root = tk.Tk()
root.title("Live Sign Language Translation")

# Create a label for displaying the video stream
video_label = tk.Label(root)
video_label.pack()

video_label2 = tk.Label(root)
video_label2.pack()

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
        image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        image_np = image_np.astype(np.uint8)

        input_tensor = tf.expand_dims(image_np, 0)
        detections = detect_fn(input_tensor)

        detected_boxes = detections['detection_boxes'][0].numpy()
        detected_classes = detections['detection_classes'][0].numpy().astype(np.int32)
        detected_scores = detections['detection_scores'][0].numpy()

        # Find the index with the highest confidence score
        top_detection_idx = np.argmax(detected_scores)

        # Update the translation text with the detected class name (top detected object)
        detected_object = category_index[detected_classes[top_detection_idx]]['name']

        # Update translation label text with detected class name
        update_translation(detected_object)

        # Visualize top detected object on the video stream label
        image_np_with_detections = np.array(frame)
        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detected_boxes,
            detected_classes,
            detected_scores,
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=5,
            min_score_thresh=0.7,
            agnostic_mode=False
        )

        img = cv2.cvtColor(cv2.resize(image_np_with_detections, (800, 600)), cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)

        video_label.img = img
        video_label.configure(image=img)

    video_label.after(10, perform_detection)  # Call the function again after 10ms

# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(files['PIPELINE_CONFIG'])
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(paths['CHECKPOINT_PATH'], 'ckpt-21')).expect_partial()




# Function to open the quiz UI in a new window
# Function to switch to the quiz UI
quiz_frame = None

# Function to capture an image from the video feed
def capture_image():
    global cap, video_label
    ret, frame = cap.read()
    if ret:
        img = cv2.cvtColor(cv2.resize(frame, (800, 600)), cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)
        video_label.img = img
        video_label.configure(image=img)


# Release video capture when the GUI is closed
def on_closing():
    cap.release()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
    
    

# Video capture setup
cap = cv2.VideoCapture(0)  # Adjust camera index as needed



# Start object detection and video stream display
perform_detection()

# Run the GUI application
root.mainloop()

# Release video capture when the GUI is closed
cap.release()
