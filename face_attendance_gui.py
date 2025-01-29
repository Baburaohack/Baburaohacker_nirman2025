import cv2
import os
import pandas as pd
from datetime import datetime
from deepface import DeepFace
from sklearn.metrics.pairwise import cosine_similarity
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from threading import Thread

# Create directories if they don't exist
os.makedirs("faces", exist_ok=True)
os.makedirs("data", exist_ok=True)

data_file = "data/known_faces.csv"
attendance_file = "data/attendance.csv"

# Initialize known faces data file
if not os.path.exists(data_file):
    pd.DataFrame(
        {"name": [], "emp_id": [], "phone": [], "embedding": [], "timestamp": []}
    ).to_csv(data_file, index=False)

# Initialize attendance data file with correct columns
if not os.path.exists(attendance_file):
    pd.DataFrame({"name": [], "in_time": [], "out_time": []}).to_csv(
        attendance_file, index=False
    )


def calculate_embedding(image_path):
    """Calculate facial embedding for the given image."""
    result = DeepFace.represent(
        image_path, model_name="Facenet", enforce_detection=False
    )
    return result[0]["embedding"]


def register_user(name, emp_id, phone):
    """Capture user face and register details"""
    user_dir = f"faces/{emp_id}"
    os.makedirs(user_dir, exist_ok=True)

    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        img_path = f"{user_dir}/profile.jpg"
        cv2.imwrite(img_path, frame)
        embedding = calculate_embedding(img_path)
        cam.release()
        cv2.destroyAllWindows()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df = pd.read_csv(data_file)
        df = pd.concat(
            [
                df,
                pd.DataFrame.from_records(
                    [
                        {
                            "name": name,
                            "emp_id": emp_id,
                            "phone": phone,
                            "embedding": embedding,
                            "timestamp": timestamp,
                        }
                    ]
                ),
            ]
        )
        df.to_csv(data_file, index=False)
        return "User registered successfully!"
    else:
        cam.release()
        cv2.destroyAllWindows()
        return "Error capturing image. Please try again."


def mark_attendance(frame):
    """Mark attendance for a user based on face verification"""
    known_faces_df = pd.read_csv(data_file)
    attendance_df = pd.read_csv(attendance_file)

    recognized = False
    frame_path = "temp_frame.jpg"
    cv2.imwrite(frame_path, frame)
    frame_embedding = calculate_embedding(frame_path)

    for _, row in known_faces_df.iterrows():
        name = row["name"]
        emp_id = row["emp_id"]
        saved_embedding = eval(row["embedding"])

        similarity = cosine_similarity([frame_embedding], [saved_embedding])[0][0]
        if similarity > 0.9:  # Threshold for face similarity
            recognized = True
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Filter by employee ID to prevent mismatch
            user_attendance = attendance_df[attendance_df["name"] == name]

            if not user_attendance.empty:
                last_entry = user_attendance.iloc[-1]

                # Check if the user has already checked in and out
                if pd.isna(last_entry["out_time"]):
                    attendance_df.loc[
                        attendance_df.index == last_entry.name, "out_time"
                    ] = current_time
                    attendance_df.to_csv(attendance_file, index=False)
                    return f"Goodbye {name}! Your OUT time is recorded."
                else:
                    return f"{name}, you have already checked in and out for today."

            # Record a new IN entry
            attendance_df = pd.concat(
                [
                    attendance_df,
                    pd.DataFrame.from_records(
                        [{"name": name, "in_time": current_time, "out_time": ""}]
                    ),
                ]
            )
            attendance_df.to_csv(attendance_file, index=False)
            return f"Welcome {name}! Your IN time is recorded."

    if not recognized:
        return "User not recognized. Please register."


class AttendanceApp(App):
    def build(self):
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        # Title label
        self.label = Label(
            text="Face Attendance System", font_size=28, bold=True, size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.label)

        # Camera feed in a rectangular box
        camera_box = BoxLayout(
            orientation="vertical", size_hint=(1, 0.5), padding=10, spacing=10
        )
        self.image = Image()
        camera_box.add_widget(self.image)
        self.layout.add_widget(camera_box)

        # Buttons in a horizontal box
        button_box = BoxLayout(orientation="horizontal", size_hint=(1, 0.1), spacing=10)

        self.register_button = Button(
            text="Register User", background_color=(0, 0.5, 1, 1)
        )
        self.register_button.bind(on_press=self.show_registration_form)
        button_box.add_widget(self.register_button)

        self.attendance_button = Button(
            text="Mark Attendance", background_color=(0, 0.8, 0, 1)
        )
        self.attendance_button.bind(on_press=self.mark_attendance)
        button_box.add_widget(self.attendance_button)

        self.layout.add_widget(button_box)

        # Start camera feed
        self.cam = cv2.VideoCapture(0)
        self.capture_thread = Thread(target=self.update_camera, daemon=True)
        self.capture_thread.start()

        return self.layout

    def update_camera(self):
        while True:
            ret, frame = self.cam.read()
            if ret:
                buf = cv2.flip(frame, 0).tobytes()
                texture = Texture.create(
                    size=(frame.shape[1], frame.shape[0]), colorfmt="bgr"
                )
                texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
                self.image.texture = texture
                self.current_frame = frame

    def show_registration_form(self, instance):
        form_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        name_input = TextInput(hint_text="Enter Name", multiline=False)
        emp_id_input = TextInput(hint_text="Enter Employee ID", multiline=False)
        phone_input = TextInput(hint_text="Enter Phone Number", multiline=False)

        form_layout.add_widget(name_input)
        form_layout.add_widget(emp_id_input)
        form_layout.add_widget(phone_input)

        submit_button = Button(text="Submit", size_hint=(1, 0.2))
        form_layout.add_widget(submit_button)

        popup = Popup(title="Register User", content=form_layout, size_hint=(0.8, 0.5))

        def on_submit(instance):
            name = name_input.text.strip()
            emp_id = emp_id_input.text.strip()
            phone = phone_input.text.strip()

            if not name or not emp_id or not phone:
                self.show_popup("Error", "All fields are required.")
                return

            message = register_user(name, emp_id, phone)
            self.show_popup("Success", message)
            popup.dismiss()

        submit_button.bind(on_press=on_submit)
        popup.open()

    def mark_attendance(self, instance):
        if hasattr(self, "current_frame"):
            result = mark_attendance(self.current_frame)
            self.show_popup("Attendance", result)
        else:
            self.show_popup("Error", "No camera frame available.")

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        popup_label = Label(text=message, halign="center", valign="middle")
        close_button = Button(text="Close", size_hint=(1, 0.2))

        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.5))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def on_stop(self):
        self.cam.release()


if __name__ == "__main__":
    AttendanceApp().run()
