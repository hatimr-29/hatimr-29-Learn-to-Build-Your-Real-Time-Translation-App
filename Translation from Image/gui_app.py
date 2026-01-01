# gui_app.py
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2

from ocr_inference import extract_text_from_image
from video_ocr import extract_text_from_video
from translator import translate_to_english

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("English Image/Video OCR → English Output")
        self.root.geometry("1000x600")

        self.display_panel = tk.Label(root, text="No Image/Video Loaded", width=50, height=20)
        self.display_panel.pack(side=tk.LEFT, padx=10, pady=10)

        right_frame = tk.Frame(root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        btn_img = tk.Button(right_frame, text="Upload Image", command=self.load_image)
        btn_img.pack(pady=5)

        btn_vid = tk.Button(right_frame, text="Upload Video", command=self.load_video)
        btn_vid.pack(pady=5)

        tk.Label(right_frame, text="Extracted English Text:").pack()
        self.text_eng = tk.Text(right_frame, height=8)
        self.text_eng.pack(fill=tk.X, padx=10)

        tk.Label(right_frame, text="Final English Output:").pack()
        self.text_final = tk.Text(right_frame, height=8)
        self.text_final.pack(fill=tk.X, padx=10)

    def show_image(self, frame):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img).resize((450, 350))
        self.photo = ImageTk.PhotoImage(img)
        self.display_panel.config(image=self.photo)

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.jpeg")])
        if not path: return

        img = cv2.imread(path)
        self.show_image(img)

        extracted = extract_text_from_image(img)
        self.text_eng.delete("1.0", tk.END)
        self.text_eng.insert(tk.END, extracted)

        final_output = translate_to_english(extracted)
        self.text_final.delete("1.0", tk.END)
        self.text_final.insert(tk.END, final_output)

    def load_video(self):
        path = filedialog.askopenfilename(filetypes=[("Videos", "*.mp4 *.avi *.mkv")])
        if not path: return

        extracted, frame = extract_text_from_video(path)
        if frame is None:
            messagebox.showerror("Error", "Unable to process video.")
            return

        self.show_image(frame)

        self.text_eng.delete("1.0", tk.END)
        self.text_eng.insert(tk.END, extracted)

        final_output = translate_to_english(extracted)
        self.text_final.delete("1.0", tk.END)
        self.text_final.insert(tk.END, final_output)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
