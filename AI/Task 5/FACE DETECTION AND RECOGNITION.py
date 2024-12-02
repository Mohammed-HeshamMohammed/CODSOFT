# To run this code, type python "path\to\FACE DETECTION AND RECOGNITION.py"  in cmd

import cv2
import face_recognition
import numpy as np
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Global variables
known_faces = []
known_names = []
exit_flag = False  # Global exit


def detect_and_recognize_faces(video_source=0):
    """
    Detect and recognize faces in a video stream.

    :param video_source: The index of the video source (default is 0)
    """
    global exit_flag
    exit_flag = False  # Reset the flag when the function starts

    video_capture = cv2.VideoCapture(video_source)

    if not video_capture.isOpened():
        messagebox.showerror("Error", "Could not open video source.")
        return

    while True:
        if exit_flag:  # Checking exit flag
            break

        ret, frame = video_capture.read()
        if not ret:
            break

        # Converting frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detecting faces
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"
            if known_faces:
                # Comparing face encoding to known faces
                matches = face_recognition.compare_faces(known_faces, face_encoding)
                face_distances = face_recognition.face_distance(known_faces, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]

            # Drawing rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Displaying frame
        cv2.imshow("Face Detection and Recognition", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

def exit_video():
    """
    Sets the exit flag to terminate video capture and closes all OpenCV windows.
    """
    global exit_flag
    exit_flag = True  # Set the flag to true to signal exit
    cv2.destroyAllWindows()  # Close all OpenCV windows

def add_known_face():
    """
    Add a known face to the list of known faces

    This function opens an OpenCV window to select an image file from the user's computer.
    It then prompts the user to enter the name of the person in the image.
    Finally, it extracts the face encoding and features from the image and adds it to the
    list of known faces.
    """
    global known_faces, known_names

    # Get the file path from the user
    file_path = filedialog.askopenfilename(title="Select an Image File")
    if not file_path:
        return

    # Get the name of the person from the user
    name = ctk.CTkInputDialog(text="Enter the name of the person:", title="Input Name").get_input()
    if not name:
        return

    # Load the image and extract the face encoding and features
    image = face_recognition.load_image_file(file_path)
    face_encodings = face_recognition.face_encodings(image)

    if face_encodings:
        # Add the face encoding and features to the list of known faces
        known_faces.append(face_encodings[0])
        known_names.append(name)
        messagebox.showinfo("Success", f"Added {name} to known faces.")
    else:
        messagebox.showerror("Error", "No face detected in the image. Please try again.")

def select_video():
    """
    Process a video file

    This function opens an OpenCV window to select a video file from the user's computer.
    It then calls the detect_and_recognize_faces function to detect and recognize faces
    in the video file.
    """
    file_path = filedialog.askopenfilename(title="Select a Video File", filetypes=[("Video Files", "*.mp4 *.avi")])
    if not file_path:
        return
    # Call the detect_and_recognize_faces function to process the video file
    detect_and_recognize_faces(video_source=file_path)

# GUI
def create_gui():
    """
    Creates the main GUI window for the Face Detection and Recognition application.

    The GUI has a modern header with a title, a content frame with three buttons to
    open the webcam, select a video file, and add a known face, and a footer with a
    message to press 'q' to stop the live video.

    :return: None
    """
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Face Detection and Recognition")
    root.geometry("600x450")

    # Add modern header
    header_frame = ctk.CTkFrame(root, height=100, corner_radius=15)
    header_frame.pack(fill="x", pady=10)

    header_label = ctk.CTkLabel(header_frame, text="Face Detection and Recognition", font=("Arial", 24, "bold"))
    header_label.pack(pady=15)

    # Main content frame
    content_frame = ctk.CTkFrame(root, corner_radius=15)
    content_frame.pack(expand=True, fill="both", padx=20, pady=10)

    # Add buttons to the content frame
    ctk.CTkButton(content_frame, text="Open Webcam", font=("Arial", 18),
                  command=lambda: detect_and_recognize_faces(0)).pack(pady=15)
    """
    Opens the webcam to detect and recognize faces.
    """
    ctk.CTkButton(content_frame, text="Select a Video", font=("Arial", 18),
                  command=select_video).pack(pady=15)
    """
    Opens an OpenCV window to select a video file from the user's computer.
    """
    ctk.CTkButton(content_frame, text="Add a Known Face", font=("Arial", 18),
                  command=add_known_face).pack(pady=15)
    """
    Opens an OpenCV window to select an image file from the user's computer and
    prompts the user to enter the name of the person in the image.
    """

    footer_label = ctk.CTkLabel(root, text="Press 'q' to stop live video", font=("Arial", 12))
    footer_label.pack(pady=10)

    root.mainloop()


create_gui()
