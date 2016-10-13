import socket
import urllib.parse

from utils import log

from routes import route_static
from routes import route_dict


# 定义一个 class 用于保存请求的数据
class Request(object):
    @staticmethod
    def parsed_path(path):
        """
        message=hello&author=gua
        {
            'message': 'hello',
            'author': 'gua',
        }
        """
        index = path.find('?')
        if index == -1:
            return path, {}
        else:
            path, query_string = path.split('?', 1)
            args = query_string.split('&')
            query = {}
            for arg in args:
                k, v = arg.split('=')
                query[k] = v
            return path, query

    @staticmethod
    def parse_header(header):
        headers = {}
        for line in header.split('\r\n')[1:]:
            if line == '':
                continue
            # log('line', line)
            k, v = line.split(': ', 1)
            headers[k] = v
        log(headers)
        return headers

    @staticmethod
    def parse_cookies(headers):
        cookies = {}
        c = headers.get('Cookie', '')
        kvs = c.split('; ')
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                cookies[k] = v
        log(cookies)
        return cookies

    def __init__(self, r):
        self.method = r.split()[0]
        self.path, self.query = self.parsed_path(r.split()[1])
        self.body = r.split('\r\n\r\n', 1)[1]
        self.headers = self.parse_header(r.split('\r\n\r\n', 1)[0])
        self.cookies = self.parse_cookies(self.headers)

    def __repr__(self):
        return '\nmethod: {}\npath: {}\nquery: {}\nbody: {}\nheaders: {}\n'.format(self.method, self.path, self.query, self.body, self.headers)

    def form(self):
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        for arg in args:
            # log('form: ', arg)
            k, v = arg.split('=')
            f[k] = v
        return f


def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    # 之前上课我说过不要用数字来作为字典的 key
    # 但是在 HTTP 协议中 code 都是数字似乎更方便所以打破了这个原则
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>404 NOT FOUND</h1>',
    }
    return e.get(code, b'')


def response_for_path(request):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    r = {
        '/static': route_static,
        # '/': route_index,
        # '/login': route_login,
        # '/messages': route_message,
    }
    r.update(route_dict)
    response = r.get(request.path, error)
    return response(request)


def run(host='', port=3000):
    """
    start the server
    """

    # init socket
    log('start at ', '{}:{}'.format(host, port))
    # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    with socket.socket() as s:
        s.bind((host, port))
        # 监听 接受 读取请求数据 解码成字符串
        while True:
            s.listen(3)
            connection, address = s.accept()
            r = connection.recv(1024)
            log(r)
            r = r.decode('utf-8')
            # log('ip and request, {}\n{}'.format(address, r))
            # 因为 chrome 会发送空请求导致 split 得到空 list
            # 所以这里判断一下防止程序崩溃
            if len(r.split()) < 2:
                log('empty')
                connection.close()
                continue
            # 解析客户端发送的request
            request = Request(r)
            # log(request)
            # 根据request构建response
            response = response_for_path(request)
            # 把响应(response)发送给客户端
            connection.sendall(response)
            # 处理完请求, 关闭连接
            connection.close()


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
