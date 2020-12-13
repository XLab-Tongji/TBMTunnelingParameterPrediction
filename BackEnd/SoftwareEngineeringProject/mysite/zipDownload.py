import os
from django.http import StreamingHttpResponse, HttpResponse


def send_zipfile(request):
    # 判断下载文件是否存在
    if not os.path.isfile(r'/Users/mawenbo/Desktop/Data.zip'):
        return HttpResponse("Sorry but Not Found the File")

    def file_iterator(file_path, chunk_size=512):
        """
        文件生成器,防止文件过大，导致内存溢出
        :param file_path: 文件绝对路径
        :param chunk_size: 块大小
        :return: 生成器
        """
        with open(file_path, mode='rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    try:
        # 设置响应头
        # StreamingHttpResponse将文件内容进行流式传输，数据量大可以用这个方法（.pdf,.mp3,.mp4等等什么样格式的文件都可以下载）
        response = StreamingHttpResponse(file_iterator(r'/Users/mawenbo/Desktop/Data.zip'))
        # 以流的形式下载文件,这样可以实现任意格式的文件下载
        response['Content-Type'] = 'application/octet-stream'
        # Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名
        response['Content-Disposition'] = 'attachment;filename={file_name}{format}'.format(
            file_name='my_zip', format=".zip")
    except:
        return HttpResponse("Sorry but Not Found the File")

    return response
