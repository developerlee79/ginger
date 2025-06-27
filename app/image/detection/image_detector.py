from abc import ABC, abstractmethod

class ImageDetector(ABC):

    @abstractmethod
    def extract_info_from_image(self, image_url):
        pass
