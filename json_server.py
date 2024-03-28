import socket
import json

from concurrent.futures import ThreadPoolExecutor

t = ThreadPoolExecutor(5)


def handle_socket(_sock, _addr):
    print('connected...')
    while True:
        res_json = _sock.recv(1024)
        res = res_json.decode('utf-8')
        # 接收消息
        # try:
        #     res_json = json.loads(res_json)
        # except Exception as e:
        #     print(e)
        # data = res_json.decode('utf-8')
        # 响应
        json_data = [
            {
                "name": "Bob",
                "age": 25,
                "city": "San Francisco"
            },
            {
                "name": "Jack",
                "age": 22,
                "city": "Paris"
            }
        ]
        json_data = json.dumps(json_data)
        http_template = f'''HTTP/1.1 200 OK
Content-Type: application/json
Access-Control-Allow-Origin:http://localhost:63342

{json_data}

'''
        # 本身是字符串，无需json.dumps转字符串
        # 一次通信获取消息即可，不需要持续通信，响应后直接关闭连接即可
        _sock.send(http_template.encode('utf-8'))
        _sock.close()
        break
#


json_server = socket.socket()
json_server.bind(('0.0.0.0', 8000))
json_server.listen()

while True:
    sock, addr = json_server.accept()
    t.submit(handle_socket, sock, addr)
