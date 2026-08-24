import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import threading
import shutil
import os
import json

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AudioCleanerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("AI Audio Cleaner")
        self.geometry("1000x750")

        self.video_path = ""

        # ==========================
        # TITLE
        # ==========================

        title = ctk.CTkLabel(
            self,
            text="AI Audio Cleaner",
            font=("Arial", 30, "bold")
        )
        title.pack(pady=15)

        # ==========================
        # VIDEO LABEL
        # ==========================

        self.video_label = ctk.CTkLabel(
            self,
            text="No Video Selected",
            font=("Arial", 14)
        )
        self.video_label.pack(pady=5)

        # ==========================
        # BUTTONS
        # ==========================

        self.upload_btn = ctk.CTkButton(
            self,
            text="Select Video",
            command=self.select_video
        )
        self.upload_btn.pack(pady=5)

        self.analyze_btn = ctk.CTkButton(
            self,
            text="Analyze Audio",
            command=self.start_analysis
        )
        self.analyze_btn.pack(pady=5)

        # ==========================
        # PROGRESS BAR
        # ==========================

        self.progress = ctk.CTkProgressBar(self)
        self.progress.pack(fill="x", padx=20, pady=10)
        self.progress.set(0)

        # ==========================
        # LAYERS
        # ==========================

        self.layers_frame = ctk.CTkFrame(self)
        self.layers_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.layer_vars = {}

        # ==========================
        # EXPORT
        # ==========================

        self.export_btn = ctk.CTkButton(
            self,
            text="Create Final Video",
            command=self.export_video
        )
        self.export_btn.pack(pady=5)

        self.open_btn = ctk.CTkButton(
            self,
            text="Open Output Folder",
            command=self.open_output
        )
        self.open_btn.pack(pady=5)

        # ==========================
        # LOGS
        # ==========================

        self.log_box = ctk.CTkTextbox(
            self,
            height=180
        )
        self.log_box.pack(
            fill="x",
            padx=20,
            pady=15
        )

    # =================================================

    def log(self, text):
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")
        self.update()

    # =================================================

    def select_video(self):

        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Video Files", "*.mp4 *.mov *.avi *.mkv")
            ]
        )

        if not file_path:
            return

        self.video_path = file_path

        os.makedirs("input", exist_ok=True)

        shutil.copy(
            file_path,
            "input/video.mp4"
        )

        self.video_label.configure(
            text=os.path.basename(file_path)
        )

        self.log("Video selected.")

    # =================================================

    def start_analysis(self):
        threading.Thread(
            target=self.analyze_audio,
            daemon=True
        ).start()

    # =================================================

    def analyze_audio(self):

        try:

            self.progress.set(0)

            self.log("Extracting audio...")
            subprocess.run(
                ["python", "app.py"],
                check=True
            )

            self.progress.set(0.30)

            self.log("Detecting sounds...")
            subprocess.run(
                ["python", "sound_detector.py"],
                check=True
            )

            self.progress.set(0.60)

            self.log("Creating layers...")
            subprocess.run(
                ["python", "layer_manager.py"],
                check=True
            )

            self.progress.set(1.0)

            self.load_layers()

            self.log("Analysis complete.")

            messagebox.showinfo(
                "Success",
                "Audio analysis completed."
            )

        except Exception as e:

            self.log(str(e))

            messagebox.showerror(
                "Error",
                str(e)
            )

    # =================================================

    def load_layers(self):

        for widget in self.layers_frame.winfo_children():
            widget.destroy()

        self.layer_vars.clear()

        title = ctk.CTkLabel(
            self.layers_frame,
            text="Detected Audio Layers",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=10)

        if not os.path.exists("layers"):
            return

        for file in os.listdir("layers"):

            if not file.endswith(".wav"):
                continue

            var = ctk.BooleanVar(value=True)

            cb = ctk.CTkCheckBox(
                self.layers_frame,
                text=file,
                variable=var
            )

            cb.pack(
                anchor="w",
                padx=20,
                pady=5
            )

            self.layer_vars[file] = var

    # =================================================

    def export_video(self):

        try:

            keep = []

            for layer, var in self.layer_vars.items():

                if var.get():
                    keep.append(layer)

            if not keep:
                messagebox.showwarning(
                    "Warning",
                    "Select at least one layer."
                )
                return

            with open(
                "user_selection.json",
                "w"
            ) as f:

                json.dump(
                    {"keep": keep},
                    f,
                    indent=4
                )

            self.log("Mixing audio...")

            subprocess.run(
                ["python", "audio_mixer.py"],
                check=True
            )

            self.log("Rendering video...")

            subprocess.run(
                ["python", "final_render.py"],
                check=True
            )

            self.log("Finished.")

            output_file = os.path.abspath(
                "output/final_video.mp4"
            )

            messagebox.showinfo(
                "Success",
                f"Video created:\n\n{output_file}"
            )

        except Exception as e:

            self.log(str(e))

            messagebox.showerror(
                "Error",
                str(e)
            )

    # =================================================

    def open_output(self):

        output_folder = os.path.abspath("output")

        if os.path.exists(output_folder):
            os.startfile(output_folder)

    # =================================================


if __name__ == "__main__":
    app = AudioCleanerApp()
    app.mainloop()