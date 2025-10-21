from pyaudio import PyAudio

class DeviceInfo:
    """
    Retrieves and stores information about all audio input/output devices
    available through a given PyAudio instance.

    This class queries the PyAudio API for all connected audio devices,
    records their information, and provides convenient accessors for:
    - The total device count
    - The default input device and its index
    - Full or partial information for any device by index
    """

    def __init__(self, p : PyAudio) -> None:
        """
        Args:
            p (pyaudio.PyAudio): PyAudio port is used to get all the device info.
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
        if device_count != len(all_device_info):
            raise RuntimeError("Device count and lenght of device info list must match.")
        
        self._device_count = device_count
        self._default_device_index = int(default_device_index)
        self._all_device_info = all_device_info

    @property
    def device_count(self) -> int:
        return self._device_count
    
    @property
    def default_device(self) -> dict:
        """
        Complete info of default device.
        """
        return self._all_device_info[self._default_device_index]
    
    @property
    def default_device_index(self) -> int:
        return self._default_device_index
    
    def get_device_info(self, index : int):
        """
        Gets complete info of device at given index.

        Args:
            index (int): Device index [0, device_count].
        """
        if index < 0 or index >= self.device_count:
            raise RuntimeError(f"Requested device index: {index} isn't available.")
        return self._all_device_info[index]
    
    def get_device_name(self, index : int) -> str:
        """
        Gets the name of the device at given index.

        Args:
            index (int): Device index [0, device_count].
        """
        if index < 0 or index >= self.device_count:
            raise RuntimeError(f"Requested device index: {index} isn't available.")
        return str(self._all_device_info[index]["name"])

