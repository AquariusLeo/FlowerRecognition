import tornado.ioloop
import tornado.web
import tornado.websocket
import base64
import os
from PIL import Image
import matplotlib.pyplot as plt
import json
import flowerRecog

#/路径处理程序
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
        
#/ajax路径处理程序
class AjaxHandler(tornado.web.RequestHandler):
    def post(self):
        # 获取base64编码，解码，保存为jpg文件
        base64str=self.get_argument("myphoto")
        base64str=base64str[23:]    # 截去前面的data:image/jpeg;base64,
        imgdata=base64.b64decode(base64str)
        f=open(os.path.join(os.path.dirname(__file__), "tmp.jpg"), "wb")
        f.write(imgdata)
        f.close()

        # 用matplotlib显示图片
        img = Image.open(os.path.join(os.path.dirname(__file__), "tmp.jpg"))
        plt.ion() # 开启interactive mode
        plt.figure("Image") # 图像窗口名称
        plt.imshow(img)
        plt.axis('on') # 关掉坐标轴为 off
        plt.title('image') # 图像题目
        plt.pause(2)
        plt.close("Image")

        # 调用识别函数，并返回结果
        result=flowerRecog.flower_recog(os.path.join(os.path.dirname(__file__), "tmp.jpg"))
        print(result)
        data={'result':result}
        self.write(json.dumps(data))

handlers=[
    (r"/",IndexHandler),
    (r"/ajax",AjaxHandler)
]

if __name__=="__main__":
    app=tornado.web.Application(handlers,static_path=os.path.join(os.path.dirname(__file__),"static"),debug=True)
    app.listen(8100)
    tornado.ioloop.IOLoop.current().start()