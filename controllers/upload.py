import os
import uuid

from configs.config import configs
from controllers.base import Base
from flask import request
from werkzeug.utils import secure_filename


class Upload(Base):

    def __init__(self):
        super().__init__()
        self.domain = configs['domain']
        self.upload_config = configs['upload']
        self.path = self.upload_config['path']
        self.ext = self.upload_config['ext']

    # 上传文件
    def upload_file(self):
        if request.method == 'POST':
            # 获取post过来的文件名称，从name=file参数中获取
            file = request.files['file']
            filename = secure_filename(file.filename)
            list_f = filename.rsplit('.', 1)
            if len(list_f) <= 1:
                return self.ret_json(10001, '请上传英文文件名')
            allow = self.allowed_file(file.filename)
            if file and allow:
                # secure_filename方法会去掉文件名中的中文(只能英文名字)
                filename = secure_filename(file.filename)
                print(filename)
                if len(filename) <= 0:
                    return self.ret_json(10002, '请上传英文文件名')
                # 因为上次的文件可能有重名，因此使用uuid保存文件
                file_name = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[1]
                file.save(os.path.join(self.path, file_name))
                file_path = self.domain + '/uploads/' + file_name
                return self.ret_json(1, 'ok', {"upload_file": file_path})
            else:
                return self.ret_json(10003, '文件类型不支持')

        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="/pyapi/upload" method=post enctype=multipart/form-data>
        <p>
            <input type=file name=file>
            <input type=submit value=Upload>
        </form>
        '''

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in self.ext
