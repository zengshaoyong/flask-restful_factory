import tornado.websocket
import tornado.web
import tornado.options
import asyncio

from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream

commands = []

config.load_kube_config()
try:
    c = Configuration().get_default_copy()
except AttributeError:
    c = Configuration()
    c.assert_hostname = False
Configuration.set_default(c)
core_v1 = core_v1_api.CoreV1Api()

api_instance = core_v1


class WebSocket(tornado.websocket.WebSocketHandler):
    # waiters = set()
    resp = ''
    user = ''
    namespace = ''
    pod = ''

    def get_compression_options(self):
        return {}

    def open(self):
        print('open')
        # self.resp.update(timeout=1)
        # if self.resp.peek_stdout():
        #     print("STDOUT: %s" % self.resp.read_stdout())
        # if self.resp.peek_stderr():
        #     print("STDERR: %s" % self.resp.read_stderr())
        # self.waiters.add(self)
        self.user = self
        # self.namespace = self.get_argument('namespace', default='default', strip=True)
        # self.pod = self.get_argument('pod', strip=True)

        exec_command = ['/bin/bash']
        self.resp = stream(api_instance.connect_get_namespaced_pod_exec,
                           'nginx-deployment-6799fc88d8-dbp8t',
                           'default',
                           command=exec_command,
                           stderr=True, stdin=True,
                           stdout=True, tty=False, _preload_content=False)
        # response = self.resp.read_stdout()
        # self.user.write_message(response)
        # print("成功了")
        # data = self.resp.read_stdout()
        # print(data)

    def on_close(self):
        print('close')

    # self.waiters.remove(self)

    def on_message(self, message):
        print(message)
        if message:
            self.resp.write_stdin(message)
            response = self.resp.readline_stdout(timeout=1)
            self.user.write_message(response)


app = tornado.web.Application([
    (r"/", WebSocket),
])

# def echo_socket(ws, path):
#     exec_command = ['/bin/sh']
#     resp = stream(api_instance.connect_get_namespaced_pod_exec,
#                   'nginx-545c8b5bf7-9drrh',
#                   'default',
#                   command=exec_command,
#                   stderr=True, stdin=True,
#                   stdout=True, tty=True,
#                   _preload_content=False)
#     while resp.is_open():
#         message = ws.recv()
#         print(message)
#         resp.write_stdin(message)
#         response = resp.read_stdout()
#         ws.send(response)
#     resp.close()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(6000)
    tornado.ioloop.IOLoop.instance().start()
