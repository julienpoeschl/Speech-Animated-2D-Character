import pyaudio

class DeviceInfo:
    def __init__(self, device_count : int, default_device_index : str | int | float, all_device_info : list[dict[str, str | int | float]]) -> None:
        if device_count != len(all_device_info):
            raise RuntimeError("Device count and lenght of device info list must match.")
        
        self._device_count = device_count
        self.default_device_index = int(default_device_index)
        self._all_device_info = all_device_info

    @property
    def device_count(self) -> int:
        return self._device_count
    
    @property
    def default_device(self) -> dict[str, str | int | float]:
        return self._all_device_info[self.default_device_index]
    
    def get_device_info(self, index : int):
        if index < 0 or index > self.device_count:
            raise RuntimeError(f"Requested device index: {index} isn't available.")
        return self._all_device_info[index]
    
    def get_device_name(self, index : int) -> str:
        if index < 0 or index > self.device_count:
            raise RuntimeError(f"Requested device index: {index} isn't available.")
        return str(self._all_device_info[index]["name"])


def get_device_info(p : pyaudio.PyAudio) -> DeviceInfo:
    """
    
    """

    device_count = p.get_device_count()

    all_device_info = []

    for i in range(device_count):
        device_info = p.get_device_info_by_index(i)
        print(f"{i}: {device_info['name']}")
        all_device_info.append(device_info)

    default_device_index = p.get_default_input_device_info()['index']
    default_device_name = p.get_default_input_device_info()['name']
    print("Default input device:", default_device_name)

    return DeviceInfo(device_count=device_count, default_device_index=default_device_index, all_device_info=all_device_info)