import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import tqdm

# from py_audio2face.audio2face import Audio2Face

import sys
sys.path.append(".")
sys.path.append("./py_audio2face")

from py_audio2face.audio2face import Audio2Face

from py_audio2face import utils

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

        self.settings_entries = {}

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

        for key in self.default_settings.keys():
            ttk.Label(self.settings_frame, text=f"{key}:").pack(anchor='nw', padx=5, pady=2)
            entry = ttk.Entry(self.settings_frame, width=15)
            entry.insert(0, str(self.default_settings[key]))
            entry.pack(anchor='nw', pady=2)
            self.settings_entries[key] = entry  # 保存输入框引用到字典



        
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


    def update_settings(self):
        for key, entry in self.settings_entries.items():
            try:
                # 更新设置字典中的值，根据实际情况转换类型
                # TODO: 感觉处理不阳间
                self.default_settings[key] = type(self.default_settings[key])(entry.get())
            except ValueError as e:
                messagebox.showerror("设置错误", f"无法更新设置 '{key}': {e}")
                continue

        # 硬编码
        self.default_settings["a2f_instance"] = "/World/audio2face/CoreFullface"

        print(self.default_settings)


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



    def execute_single(self):

        self.update_settings()

        file_dir = self.dir_entry.get()
        file_name = self.file_entry.get()

        file_path = os.path.join(file_dir,file_name)

        output_dir = self.output_dir_entry.get()
        if file_path and output_dir:
            self.process_single_file(file_path, output_dir)

    def execute_batch(self):

        self.update_settings()

        dir_path = self.dir_entry.get()
        output_dir = self.output_dir_entry.get()
        if dir_path and output_dir:
            self.process_directory(dir_path, output_dir)


    def process_single_file(self, file_path, output_dir):
        # Here you can use your a2f.audio2face_single with proper parameters
        print("Processing single file:", file_path)

        self.a2f.init_a2f()

        self.a2f.set_root_path(file_path)
        self.a2f.set_track(file_path)

        output_path = os.path.join(output_dir,os.path.basename(file_path))


        if not os.path.isabs(output_path):
            output_path = os.path.join(os.getcwd(), output_path)

        if not os.path.isdir(os.path.dirname(output_path)):
            print(f"creating output dir: {output_path}")
            os.makedirs(os.path.dirname(output_path))


        self.a2f.generate_emotion_keys(self.default_settings)

        self.a2f.export_blend_shape(output_path=output_path)

        # print(self.a2f.get_emotion())

        messagebox.showinfo("转换完成", f"文件 '{os.path.basename(file_path)}' 已转换完成")


    def process_directory(self, dir_path, output_dir):
        # Here you can iterate over the directory files and apply audio2face_folder logic
        print("Processing directory:", dir_path)
        # self.a2f.audio2face_folder(dir_path, output_dir, fps=60, emotion=True)


        self.a2f.init_a2f()
        self.a2f.set_root_path(dir_path)

        # 设置自动填充情绪
        # print(self.a2f.a2e_set_settings_from_dict(settings=self.default_settings))
        # print(self.a2f.set_auto_emotion())

        audio_files = utils.get_files_in_dir(dir_path, [".wav", ".mp3"])
        audio_files_tqdm = tqdm.tqdm(audio_files)

        for af in audio_files_tqdm:
            audio_files_tqdm.set_description(f"Processing {af}")

            self.a2f.set_track(af)

            # outfile name will be base file name of af_a2f_animation
            outfile_name, ext = os.path.basename(af).rsplit(".", 1)
            outfile_name = f"{output_dir}/{outfile_name}_a2f_animation"

            # avoid non absolute paths
            if not os.path.isabs(outfile_name):
                outfile_name = os.path.join(os.getcwd(), outfile_name)

            if not os.path.isdir(os.path.dirname(outfile_name)):
                print(f"creating output dir: {outfile_name}")
                os.makedirs(os.path.dirname(outfile_name))

            self.a2f.generate_emotion_keys(self.default_settings)
            self.a2f.export_blend_shape(output_path=outfile_name)
            print(self.a2f.get_emotion())


        messagebox.showinfo("转换完成", f"文件夹 '{os.path.basename(dir_path)}' 已转换完成")



if __name__ == "__main__":
    app = Audio2FaceApp()
    app.mainloop()
