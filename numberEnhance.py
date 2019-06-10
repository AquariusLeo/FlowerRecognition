import os
import tensorflow as tf

global count # 全局变量，用于统计已处理张数
count=1

def enhance(filepath, filename):
    global count

    with tf.Session() as sess:
        # for filename in filelist:
        print(os.path.join(filepath, filename)+'  已处理：%d张'%(count))
        count+=1

        #读取图像
        image_raw_data=tf.gfile.GFile(os.path.join(filepath, filename), 'rb').read()
        image=tf.image.decode_jpeg(image_raw_data)
        image=tf.image.convert_image_dtype(image, dtype=tf.uint8)

        #中心区域裁剪
        crop_image=tf.image.central_crop(image, 0.9)

        #缩放至299*299
        resize_image=tf.image.resize_images(crop_image, [299,299], method=1)
        substrs=filename.split('.', 1) # 获取文件名
        savepath=filepath.replace('original_photos', 'flower_photos') # 获取存放路径
        image_raw_data=tf.image.encode_jpeg(resize_image).eval()
        with tf.gfile.GFile(os.path.join(savepath, substrs[0]+'_resize.jpg'), 'wb') as t:
            t.write(image_raw_data) # 保存图像

        #上下反转
        updown_image=tf.image.flip_up_down(resize_image)
        image_raw_data=tf.image.encode_jpeg(updown_image).eval()
        with tf.gfile.GFile(os.path.join(savepath, substrs[0]+'_updown.jpg'), 'wb') as t:
            t.write(image_raw_data) # 保存图像

        #左右反转
        leftright_image=tf.image.flip_left_right(resize_image)
        image_raw_data=tf.image.encode_jpeg(leftright_image).eval()
        with tf.gfile.GFile(os.path.join(savepath, substrs[0]+'_leftright.jpg'), 'wb') as t:
            t.write(image_raw_data) # 保存图像

        #对角线反转
        transpose_image=tf.image.transpose_image(resize_image)
        image_raw_data=tf.image.encode_jpeg(transpose_image).eval()
        with tf.gfile.GFile(os.path.join(savepath, substrs[0]+'_transpose.jpg'), 'wb') as t:
            t.write(image_raw_data) # 保存图像
        
        #亮度、饱和度、色相随机调整
        brightness_image=tf.image.random_brightness(resize_image, 0.3) #亮度随机调整
        saturation_image=tf.image.random_saturation(brightness_image, 0.5, 1.5) #饱和度随机调整
        hue_image=tf.image.random_hue(saturation_image, 0.2) #色相随机调整
        image_raw_data=tf.image.encode_jpeg(hue_image).eval()
        with tf.gfile.GFile(os.path.join(savepath, substrs[0]+'_random.jpg'), 'wb') as t:
            t.write(image_raw_data) # 保存图像

def main():
    global count
    flowerlist=('牵牛花', '三色堇', '石竹', '万寿菊', '月季')
    for name in flowerlist:
        path = os.path.join(os.path.dirname(__file__), 'original_photos', name)
        print('\n\n=====================================\n正在处理：'+name+'   路径：'+path)
        for root,dirs,files in os.walk(path):
            for filename in files:
                enhance(path, filename)
        
if __name__ == '__main__':
    main()