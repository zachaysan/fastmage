import tornado.ioloop
import tornado.web
from tornado.options import define, options, logging
import os
import uuid
from pprint import pprint

define("port", default=8877, help="run on the given port", type=int)

settings = {
    "debug": True,
}

server_settings = {
    "xheaders" : True,
}

class ImageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('fastmage.html')

    def post(self):
        def filewriter(comlink_file, node, file_path=None):
            if not file_path:
                file_path = os.path.join(os.path.dirname(__file__), "uploads")
            filename = os.path.join(file_path, str(uuid.uuid1()))
            f = open(filename, 'wb')
            f.write(comlink_file)
            f.close
            return filename
        filename = filewriter(self.request.files['comlink_file'][0]['body'])
        self.set_header("Content-Type", "text/plain")
        self.write("file saved as " + filename " user: " + node)

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}

application = tornado.web.Application([
    (r'/images', ImageHandler),
], **settings)

def main():
    tornado.options.parse_command_line()
    logging.info("Starting Tornado web server on http://localhost:%s" % options.port)
    application.listen(options.port, **server_settings)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
