from library.dbmanager import DbManager
from models.base import Base


class UploadModel(Base):
    def __init__(self):
        super().__init__()
        self.db = DbManager()

    def add_file(self):
        pass
