from abc import ABC, abstractmethod

class DeviceInfoFinder(ABC):

    @abstractmethod
    def get_device_list(self, category, page, size):
        pass

    @abstractmethod
    def get_recommend_devices(self, search_query):
        pass

    @abstractmethod
    def get_device_info(self, device_id):
        pass

    @abstractmethod
    def find_device_info(self, manufacturer, model_code):
        pass
