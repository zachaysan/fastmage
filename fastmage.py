import tornado.ioloop
import tornado.web
import os
import uuid
from pprint import pprint

class ImageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('fastmage.html')

    def post(self):
        def filewriter(comlink_file, file_path=None):
            if not file_path:
                file_path = os.path.join(os.path.dirname(__file__), "uploads")
            filename = os.path.join(file_path, str(uuid.uuid1()))
            f = open(filename, 'wb')
            f.write(comlink_file)
            f.close
            return filename
        filename = filewriter(self.request.files['comlink_file'][0]['body'])
        self.set_header("Content-Type", "text/plain")
        self.write("file saved as " + filename)

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}

application = tornado.web.Application([
    (r'/', ImageHandler),
], **settings)

def main():
    application.listen(8877)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
