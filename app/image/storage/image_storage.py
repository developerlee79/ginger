from abc import ABC, abstractmethod


class ImageStorage(ABC):

    @abstractmethod
    def upload_file(self, contents, filename):
        pass
