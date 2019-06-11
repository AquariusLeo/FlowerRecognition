import numpy as np
import tensorflow as tf
import os

# 下载的谷歌训练好的inception-v3模型文件名
MODEL_FILE = 'inceptionV3/tensorflow_inception_graph.pb'
# 保存训练数据通过瓶颈层后提取的特征向量
TRAIN_FILE = 'train_dir/model.pb'
# inception-v3 模型中代表瓶颈层结果的张量名称
BOTTLENECK_TENSOR_NAME = 'pool_3/_reshape:0'
# 图像输入张量所对应的名称
JPEG_DATA_TENSOR_NAME = 'DecodeJpeg/contents:0'
# inception-v3 模型瓶颈层的节点个数
BOTTLENECK_TENSOR_SIZE = 2048
# 定义神经网路的设置
N_CLASSES = 5
# 处理过的图片文件地址
PROCESSED_IMAGES = 'flower_processed_data.npy'

# 加载已训练好的inception-v3模型
def create_inception_graph():
    with tf.Graph().as_default() as graph:
        with tf.gfile.GFile(os.path.join(os.path.dirname(__file__), MODEL_FILE), 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            bottleneck_tensor, jpeg_data_tensor = tf.import_graph_def(graph_def, name='', return_elements=[BOTTLENECK_TENSOR_NAME, JPEG_DATA_TENSOR_NAME])
    return graph, bottleneck_tensor, jpeg_data_tensor

# 加载迁移学习后的模型
def create_trained_graph():
    with tf.Graph().as_default() as graph:
        with tf.gfile.GFile(os.path.join(os.path.dirname(__file__), TRAIN_FILE), 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            BottleneckInputPlaceholder_tensor, final_tensor = tf.import_graph_def(graph_def, name='', return_elements=['BottleneckInputPlaceholder:0', 'output/prob:0'])
    return graph, BottleneckInputPlaceholder_tensor, final_tensor

# 花卉识别函数
def flower_recog(filepath):
    graph1, bottleneck_tensor, jpeg_data_tensor = create_inception_graph()
    with tf.Session(graph=graph1) as sess:
        sess.run(tf.global_variables_initializer())
        image_raw_data = tf.gfile.GFile(filepath, 'rb').read()
        image_value = sess.run(bottleneck_tensor, {jpeg_data_tensor:image_raw_data})
        image_value = np.squeeze(image_value)
    
    graph2, BottleneckInputPlaceholder_tensor, final_tensor = create_trained_graph()
    with tf.Session(graph=graph2) as sess:
        sess.run(tf.global_variables_initializer())
        final = sess.run(final_tensor, {BottleneckInputPlaceholder_tensor:[image_value]})
        print(final)
        result = np.argmax(final)

    # 获取标签值
    processed_images=np.load(os.path.join(os.path.dirname(__file__), PROCESSED_IMAGES))
    labels=processed_images[6]
    return labels[result]

def main():
    res=flower_recog('tmp.jpg')
    print(res)

if __name__ == '__main__':
    main()