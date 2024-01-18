import tkinter as tk
import cv2
import os
import numpy as np
from PIL import Image, ImageTk
from object_detection.utils import label_map_util
from object_detection.utils import config_util
from object_detection.builders import model_builder
import tensorflow as tf
import time


files = {
    'PIPELINE_CONFIG': os.path.join('Tensorflow', 'workspace', 'models', 'my_ssd_mobnet', 'pipeline.config'),
}

paths = {
    'CHECKPOINT_PATH': os.path.join('Tensorflow', 'workspace', 'models', 'my_ssd_mobnet')
}

# Load label map and create category index
label_map_path = '/home/ronit/Documents/SOC/sign langauge detector/TFODCourse/Tensorflow/workspace/annotations/label_map.pbtxt'
category_index = label_map_util.create_category_index_from_labelmap(label_map_path)

# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(files['PIPELINE_CONFIG'])
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(paths['CHECKPOINT_PATH'], 'ckpt-21')).expect_partial()

# Load TensorFlow SavedModel for object detection
model_path = '/home/ronit/Documents/SOC/sign langauge detector/TFODCourse/Tensorflow/workspace/models/my_ssd_mobnet/export/saved_model'
detect_fn = tf.saved_model.load(model_path)


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

class QuizApp:
    def __init__(self, window, window_title, class_names_list, detect_fn, category_index, confidence_threshold=0.7,
                 detection_time_threshold=5):
        self.window = window
        self.window.title(window_title)
        self.detect_fn = detect_fn
        self.category_index = category_index
        self.current_class_name = None
        self.confidence_threshold = confidence_threshold
        self.detection_time_threshold = detection_time_threshold
        self.detected_letter = None  # Store detected letter as an instance variable

        self.vid = cv2.VideoCapture(0)

        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.grid(row=0, column=0)

        self.captured_canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.captured_canvas.grid(row=0, column=1)

        self.btn_start_quiz = tk.Button(window, text="Start Quiz", width=50, command=self.start_quiz)
        self.btn_start_quiz.grid(row=2, column=0, columnspan=2)

        self.btn_end_quiz = tk.Button(window, text="End Quiz", width=50, command=self.end_quiz, state=tk.DISABLED)
        self.btn_end_quiz.grid(row=3, column=0, columnspan=2)

        self.btn_capture = tk.Button(window, text="Capture Image", width=50, command=self.capture_image, state=tk.DISABLED)
        self.btn_capture.grid(row=4, column=0, columnspan=2)

        self.question_label = tk.Label(window, text="Your question here", font=("Arial", 20))
        self.question_label.grid(row=1, column=0, columnspan=2)

        self.detected_letter_label = tk.Label(window, text="Detected Letter")
        self.detected_letter_label.grid(row=5, column=0, columnspan=2)

        self.btn_next = tk.Button(window, text="Next", width=50, command=self.next_question, state=tk.DISABLED)
        self.btn_next.grid(row=6, column=0, columnspan=2)

        self.class_names_iter = iter(class_names_list)

        self.score = 0  # Initialize score
        self.question_number = 1  # Initialize question number

        self.score_label = tk.Label(window, text="Score: 0", font=("Arial", 16))
        self.score_label.grid(row=7, column=0, columnspan=2)

        self.btn_skip = tk.Button(window, text="Skip", width=50, command=self.skip_question, state=tk.DISABLED)
        self.btn_skip.grid(row=8, column=0, columnspan=2)

        self.start_time = None  # Variable to store the start time
        self.total_time = 0  # Variable to store the total time taken
        self.timer_label = tk.Label(window, text="Time: 0s", font=("Arial", 16))
        self.timer_label.grid(row=9, column=0, columnspan=2)

        self.delay = 15
        self.update()

        self.window.mainloop()

    def start_quiz(self):
        # Enable buttons and start the quiz
        self.btn_end_quiz.config(state=tk.NORMAL)
        self.btn_next.config(state=tk.NORMAL)
        self.btn_skip.config(state=tk.NORMAL)
        self.btn_capture.config(state=tk.NORMAL)

        # Reset variables for a new quiz
        self.score = 0
        self.question_number = 1
        self.start_time = time.time()

        # Start the first question
        self.next_question()

    def end_quiz(self):
        # Display the total time taken to complete the quiz
        self.total_time = time.time() - self.start_time
        self.timer_label.config(text=f"Total Time: {int(self.total_time)}s")
        self.question_label.config(text="Quiz completed! Thank you.")
        self.btn_next.config(state=tk.DISABLED)
        self.btn_skip.config(state=tk.DISABLED)
        self.btn_capture.config(state=tk.DISABLED)
        self.start_time = None  # Stop the timer

    def next_question(self):
        try:
            self.current_class_name = next(self.class_names_iter)
            self.question_label.config(text=f"What is the sign for {self.current_class_name}?")

            # Reset detected letter for the new question
            self.detected_letter = None

            # Update score label and enable the "Skip" button
            self.score_label.config(text=f"Score: {self.score}")
            self.btn_skip.config(state=tk.NORMAL)

            # Disable the "Next" button until the letter is detected and matches the current quiz letter
            self.btn_next.config(state=tk.DISABLED)
        except StopIteration:
            # All questions are answered, end the quiz
            self.end_quiz()

    def skip_question(self):
        # Update question number and reset detected letter for the skipped question
        self.question_number += 1
        self.current_class_name = next(self.class_names_iter)
        self.question_label.config(text=f"What is the sign for {self.current_class_name}?")
        self.detected_letter = None

        # Disable the "Next" button until the letter is detected and matches the current quiz letter
        self.btn_next.config(state=tk.DISABLED)

        # Update score label and enable the "Skip" button
        self.score_label.config(text=f"Score: {self.score}")
        self.btn_skip.config(state=tk.NORMAL)

    def capture_image(self):
        ret, frame = self.vid.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            detected_letter = self.detect_letters_in_video(frame_rgb)

            self.detected_letter = detected_letter
            self.detected_letter_label.config(text=f"Detected letter: {detected_letter}")
            self.captured_photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
            self.captured_canvas.create_image(0, 0, image=self.captured_photo, anchor=tk.NW)

            # Enable the "Next" button only if the detected letter matches the current quiz letter
            if self.detected_letter.lower() == self.current_class_name.lower():
                self.btn_next.config(state=tk.NORMAL)
                self.score += 1  # Increase score if the detected letter is correct
                self.score_label.config(text=f"Score: {self.score}")
            else:
                self.btn_next.config(state=tk.DISABLED)

    def detect_letters_in_video(self, image_np):
        input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0))
        detections = self.detect_fn(input_tensor)

        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
        detections['num_detections'] = num_detections

        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        detected_classes = detections['detection_classes']

        adjusted_detected_classes = detected_classes

        if adjusted_detected_classes[0] in self.category_index:
            detected_letter = self.category_index[adjusted_detected_classes[0]]['name']
        else:
            detected_letter = "Unknown"

        return detected_letter

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

            detected_letter = self.detect_letters_in_video(frame_rgb)
            self.detected_letter_label.config(text=f"Detected letter: {detected_letter}")

        # Update the timer label
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            self.timer_label.config(text=f"Time: {int(elapsed_time)}s")

        self.window.after(self.delay, self.update)


# Create a window and pass it to the Application object
QuizApp(tk.Tk(), "Quiz App", class_names_list, detect_fn, category_index)
