# from customtkinter import *
# import cv2
# from PIL import Image, ImageTk
# import threading

# # print("Hello World")

# def button_event():
#     print("button pressed")

# def play_video():
#     def video_loop():
#         cap = cv2.VideoCapture("your_video.mp4")  # Replace with your video file path
#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break  # Stop if the video ends
#             # Convert the frame to RGB and resize it for tkinter
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             frame = cv2.resize(frame, (300, 200))  # Set video size
#             img = ImageTk.PhotoImage(Image.fromarray(frame))
#             label.configure(image=img)
#             label.image = img

#         cap.release()

#     # Run the video in a separate thread
#     video_thread = threading.Thread(target=video_loop)
#     video_thread.daemon = True
#     video_thread.start()

# def hover_enter(event):
#     # Enlarge the button and start playing the video
#     btn1.configure(width=200, height=50, fg_color="#4158D0")
#     play_video()

# def hover_leave(event):
#     # Reset the button size
#     btn1.configure(width=150, height=40, fg_color="#C850C0")
#     label.configure(image="")  # Clear the video frame


# app = CTk()
# app.geometry("500x500")
# app.title("Some Title")

# btn1 = CTkButton(master=app, text="Don't Click Me", fg_color="#C850C0", hover_color="#4158D0",command=button_event)
# btn1.place(relx=0.5, rely=0.5, anchor="center")


# app.mainloop()
from customtkinter import *
import cv2
from PIL import Image
import threading

def play_video():
    def video_loop():
        cap = cv2.VideoCapture("Portfolio_templates/portfolio_videos/video 1 - 1737262353213.mp4")  # Replace with your video file path
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break  # Stop if the video ends
            # Convert the frame to RGB and resize it
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (300, 200))  # Set video size
            img = Image.fromarray(frame)  # Convert frame to PIL Image
            ctk_img = CTkImage(img, size=(300, 200))  # Convert PIL Image to CTkImage
            video_label.configure(image=ctk_img)
            video_label.image = ctk_img

        cap.release()

    # Run the video in a separate thread
    video_thread = threading.Thread(target=video_loop)
    video_thread.daemon = True
    video_thread.start()

def hover_enter(event):
    # Enlarge the button and start playing the video
    btn1.configure(width=200, height=50, fg_color="#4158D0")
    play_video()

def hover_leave(event):
    # Reset the button size
    btn1.configure(width=150, height=40, fg_color="#C850C0")
    video_label.configure(image=None)  # Clear the video frame

# Create the app
app = CTk()
app.geometry("500x500")
app.title("Hover Video Example")

# Create a CTkLabel to display the video
video_label = CTkLabel(app, text="", bg_color="black", width=300, height=200)
video_label.place(relx=0.5, rely=0.4, anchor="center")

# Create the button with hover effects
btn1 = CTkButton(master=app, text="Hover Over Me", fg_color="#C850C0", hover_color="#FF5733", width=150, height=40)
btn1.place(relx=0.5, rely=0.7, anchor="center")

# Bind hover events
btn1.bind("<Enter>", hover_enter)
btn1.bind("<Leave>", hover_leave)

app.mainloop()
