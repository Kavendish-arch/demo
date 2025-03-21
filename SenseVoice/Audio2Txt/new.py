import sounddevice as sd
import soundfile as sf



def check_device_channels(device_id):
    device_info = sd.query_devices(device_id)
    max_input_channels = device_info['max_input_channels']
    print(f"Device {device_id} supports up to {max_input_channels} input channels.")
    return max_input_channels



def record_audio(duration, device_id, samplerate=44100):
    device_info = sd.query_devices(device_id)
    max_input_channels = device_info['max_input_channels']
    print("设备信息", max_input_channels,device_info , )

    # channels =
    channels = min(2, max_input_channels)  # 确保不超过设备支持的最大通道数
    if( channels > max_input_channels):
        raise Exception("设备不支持立体声录音")
        # return "设备不支持立体声录音"
    """
    sd.rec 是 sounddevice 模块中的一个函数，用于录制音频数据。以下是该函数在选中代码中的参数解释：
    int(duration * samplerate)：计算录制的总样本数，等于录制时长（秒）乘以采样率（每秒样本数）。
    samplerate=samplerate：指定采样率，表示每秒采集的音频样本数，单位为 Hz。
    channels=2：指定录制的声道数，2 表示立体声（双声道），1 表示单声道。
    dtype='float32'：指定录制数据的格式，float32 表示每个样本使用 32 位浮点数存储。
    device=device_id：指定录音设备的 ID，如果为 None，则使用默认设备。
    """
    myrecording = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=channels,
        dtype='float32',
        device=device_id
    )
    sd.wait()
    return myrecording
# # 示例：检查 device_id=1 的通道数
# max_channels = check_device_channels(1)
# if max_channels < 2:
#     print("The device does not support stereo recording (2 channels).")

# # 调用示例
# record_system_audio('../audioWs/output_xitong.wav', duration=10, device_id=1)


def record_system_audio(filename, duration=5, samplerate=400, device_id=None):
    print("可用设备：")
    print(sd.query_devices())

    if device_id is None:
        print("未指定设备ID，使用默认设备。")
    else:
        print(f"使用设备ID: {device_id}")

    print("开始录制系统音频...")

    myrecording = record_audio(int(duration * samplerate),
                               samplerate=samplerate, device_id=device_id)
    print("录制完成。")

    sd.play(myrecording, samplerate)

    sf.write(filename, myrecording, samplerate)
    print(f"音频已保存为 {filename}")

if __name__ == "__main__":
    record_system_audio('../audioWs/output_xitong.wav', duration=10, device_id=39)  # 录制10秒的系统音频，使用设备ID为1
