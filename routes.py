from utils import log
from models import Message
from models import User


def template(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def response_with_headers(headers):
    """
Content-Type: text/html
Set-Cookie: user=gua
    """
    header = 'HTTP/1.x 210 VERY OK\r\n'
    header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    return header


def route_index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.x 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_login(request):
    headers = {
        'Content - Type': 'text / html',
        # 'Set-Cookie': 'height=169; gua=1; pwd=2; Path=/',
    }

    username = request.cookies.get('user', '游客')
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_login():
            headers['Set-Cookie'] = 'user={}'.format(u.username)
            result = '登录成功'
        else:
            result = '用户名或者密码错误'
    else:
        result = ''
    body = template('login.html')
    body = body.replace('{{result}}', result)
    body = body.replace('{{username}}', username)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_register(request):
    """
    注册页面的路由函数
    """
    header = 'HTTP/1.x 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_message(request):
    """
    消息页面的路由函数
    """
    log('本次请求的 method', request.method)
    if request.method == 'POST':
        form = request.form()
        msg = Message(form)
        log('post', form)
        msg.save()
    result = '<br><pre>{}</pre>'.format(Message.all())
    header = 'HTTP/1.x 200 OK\r\nContent-Type: text/html\r\n'
    # body = '<h1>消息版</h1>'
    body = template('message.html')
    # msgs = '<br>'.join([str(m) for m in message_list])
    body = body.replace('{{messages}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.x 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


def route_v2ex(request):
    path = 'homework12/v2ex.html'
    with open(path, 'rb') as f:
        header = b'HTTP/1.x 200 OK\r\nContent-Type: html\r\n\r\n'
        page = header + f.read()
        return page


def route_avatar1(request):
    filename = request.path
    path = 'homework12/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.x 200 OK\r\nContent-Type: image\r\n\r\n'
        img = header + f.read()
        return img


def route_avatar2(request):
    filename = request.path
    path = 'homework12/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.x 200 OK\r\nContent-Type: image\r\n\r\n'
        img = header + f.read()
        return img


def route_logo(request):
    filename = request.path
    log(request.path)
    path = 'homework12/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.x 200 OK\r\nContent-Type: image\r\n\r\n'
        img = header + f.read()
        return img


def route_search(request):
    filename = request.path
    path = 'homework12/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.x 200 OK\r\nContent-Type: image\r\n\r\n'
        img = header + f.read()
        return img


def route_icon(request):
    filename = request.path
    path = 'homework12/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.x 200 OK\r\nContent-Type: image\r\n\r\n'
        img = header + f.read()
        return img


route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    '/messages': route_message,
    '/v2ex': route_v2ex,
    '/avatar1.png': route_avatar1,
    '/avatar2.png': route_avatar2,
    '/logo.png': route_logo,
    '/search.png': route_search,
    '/icon.png': route_icon,
}