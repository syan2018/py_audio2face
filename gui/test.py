from py_audio2face import Audio2Face
import os


a2f = Audio2Face()


audio_file_path = "F:/PBZ/Sound/WwiseProject_YZRL/Originals/Voices/Chinese/Plot/VS2/1Vo_Plot_JiangHuRenShi_12.wav"
output_path = "F:/PythonScripts/Audio2FaceTest3/JHRS.usd"

default_settings = {
    "a2f_instance": "/World/audio2face/CoreFullface",
    "a2e_window_size": 1.4,
    "a2e_stride": 1,
    "a2e_emotion_strength": 0.5,
    "a2e_smoothing_exp": 0.0,
    "a2e_max_emotions": 5,
    "a2e_contrast": 1.0,
}


a2f.init_a2f()

a2f.set_root_path(audio_file_path)
a2f.set_track(audio_file_path)

if not os.path.isabs(output_path):
    output_path = os.path.join(os.getcwd(), output_path)

if not os.path.isdir(os.path.dirname(output_path)):
    print(f"creating output dir: {output_path}")
    os.makedirs(os.path.dirname(output_path))


a2f.generate_emotion_keys(default_settings)

a2f.export_blend_shape(output_path=output_path)

print(a2f.get_emotion(0))

