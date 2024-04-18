import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

from py_audio2face.audio2face import Audio2Face

class Audio2FaceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Audio to Face Animation")
        # self.geometry("700x500")

        # Audio2Face instance
        self.a2f = Audio2Face()
        
        # Default settings
        self.default_settings = {
            "a2e_window_size": 1.4,
            "a2e_stride": 1,
            "a2e_emotion_strength": 0.5,
            "a2e_smoothing_exp": 0.0,
            "a2e_max_emotions": 5,
            "a2e_contrast": 1.0,
        }


        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        # Creating frames for layout
        self.left_frame = ttk.Frame(self, padding="10")
        self.left_frame.grid(row=0, column=0, sticky="nswe")

        self.right_frame = ttk.Frame(self, padding="10")
        self.right_frame.grid(row=0, column=1, sticky="nswe", padx=(10, 0))

        # Adding a frame for directory and file selection in left frame
        self.input_frame = ttk.LabelFrame(self.left_frame, text="输入", padding="10")
        self.input_frame.pack(fill='x', expand=True, pady=10)

        ttk.Label(self.input_frame, text="输入文件夹:").pack(anchor='nw')
        self.dir_entry = ttk.Entry(self.input_frame, width=50)
        self.dir_entry.pack(anchor='nw', expand=True, fill='x', pady=2)
        ttk.Button(self.input_frame, text="浏览", command=self.browse_directory).pack(anchor='nw', pady=2)

        ttk.Label(self.input_frame, text="（可选）选择音频文件:").pack(anchor='nw')
        self.file_entry = ttk.Entry(self.input_frame, width=50)
        self.file_entry.pack(anchor='nw', expand=True, fill='x', pady=2)
        ttk.Button(self.input_frame, text="浏览", command=self.browse_file).pack(anchor='nw', pady=2)

        # Adding a frame for output directory selection in left frame
        self.output_frame = ttk.LabelFrame(self.left_frame, text="输出", padding="10")
        self.output_frame.pack(fill='x', expand=True, pady=10)

        ttk.Label(self.output_frame, text="输出文件夹:").pack(anchor='nw')
        self.output_dir_entry = ttk.Entry(self.output_frame, width=50)
        self.output_dir_entry.pack(anchor='nw', expand=True, fill='x', pady=2)
        ttk.Button(self.output_frame, text="浏览", command=self.browse_output_directory).pack(anchor='nw', pady=2)

        # Adding a frame for action buttons
        self.action_frame = ttk.Frame(self.left_frame, padding="10")
        self.action_frame.pack(fill='x', expand=True, pady=20)

        # Buttons for single and batch processing
        self.single_process_button = ttk.Button(self.action_frame, text="单个生成", command=self.execute_single)
        self.single_process_button.pack(side='left', padx=10)

        self.batch_process_button = ttk.Button(self.action_frame, text="批量生成", command=self.execute_batch)
        self.batch_process_button.pack(side='right', padx=10)


        # Settings in right frame
        self.settings_frame = ttk.LabelFrame(self.right_frame, text="设置参数", padding="10")
        self.settings_frame.pack(fill='x', expand=True, pady=10)

        for key, value in self.default_settings.items():
            ttk.Label(self.settings_frame, text=f"{key}:").pack(anchor='nw')
            entry = ttk.Entry(self.settings_frame, width=15)
            entry.insert(0, str(value))
            entry.pack(anchor='nw', pady=2)


        
        # 配置grid行列权重
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # 调整左右两个frame的权重分配
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # 确保左右Frame可以展开填满空间
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=1)

        # 配置Frame内的所有元素，使其在垂直方向上填充空间
        self.input_frame.pack(fill='both', expand=True)
        self.output_frame.pack(fill='both', expand=True)
        self.action_frame.pack(fill='both', expand=True)
        self.settings_frame.pack(fill='both', expand=True)

        # 可以为左右Frame设置最小宽度，避免过度压缩
        self.left_frame.grid_propagate(False)
        self.right_frame.grid_propagate(False)
        self.left_frame.config(width=350)
        self.right_frame.config(width=350)


        
    def browse_output_directory(self):
        dirpath = filedialog.askdirectory()
        if dirpath:
            self.output_dir_entry.delete(0, tk.END)
            self.output_dir_entry.insert(0, dirpath)


    def browse_directory(self):
        dirpath = filedialog.askdirectory()
        if dirpath:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, dirpath)
            self.file_entry.delete(0, tk.END)


    def browse_file(self):
        dirpath = self.dir_entry.get()
        filepath = filedialog.askopenfilename(initialdir=dirpath, filetypes=[("Audio Files", "*.wav *.mp3")])
        if filepath:
            filename = os.path.basename(filepath)  # 获取文件名部分
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filename)  # 只插入文件名


    def execute(self):
        # Get file and directory paths from entries
        file_path = self.file_entry.get()
        dir_path = self.dir_entry.get()

        if file_path:
            self.process_single_file(file_path)
        if dir_path:
            self.process_directory(dir_path)

    def execute_single(self):
        file_path = self.file_entry.get()
        output_dir = self.output_dir_entry.get()
        if file_path and output_dir:
            self.process_single_file(file_path, output_dir)

    def execute_batch(self):
        dir_path = self.dir_entry.get()
        output_dir = self.output_dir_entry.get()
        if dir_path and output_dir:
            self.process_directory(dir_path, output_dir)


    def process_single_file(self, file_path, output_dir):
        # Here you can use your a2f.audio2face_single with proper parameters
        print("Processing single file:", file_path)

    def process_directory(self, dir_path, output_dir):
        # Here you can iterate over the directory files and apply audio2face_folder logic
        print("Processing directory:", dir_path)



if __name__ == "__main__":
    app = Audio2FaceApp()
    app.mainloop()
