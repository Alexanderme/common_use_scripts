import PIL.Image as Image
import os


# 获取图片大小
def get_size(path):
    for img_pic in os.listdir(path):
        if img_pic.endswith(".jpg"):
            img_pic = os.path.join(path, img_pic)
            print(img_pic)
            img = Image.open(img_pic)
            imgSize = img.size  # 图片的长和宽
            maxSize = max(imgSize)  # 图片的长边
            minSize = min(imgSize)  # 图片的短边
            yield (maxSize, minSize, img_pic)


# 定义图像拼接函数
def image_compose(image_names, save_path, IMAGES_PATH):
    image_datas = get_size(IMAGES_PATH)
    count = 0
    num = 0
    for maxSize, minSize, img_pic in image_datas:
        to_image = Image.new('RGB', (IMAGE_COLUMN * maxSize, IMAGE_ROW * minSize))
        for y in range(1, IMAGE_ROW + 1):
            for x in range(1, IMAGE_COLUMN + 1):
                try:
                    from_image = Image.open(os.path.join(IMAGES_PATH, image_names[num])).resize(
                        (maxSize, minSize), Image.ANTIALIAS)
                    to_image.paste(from_image, ((x - 1) * maxSize, (y - 1) * minSize))
                    img = image_names[num].split('.')[0]
                    count += 1
                    num += 1
                    if count % 3 == 0:
                        print(count / 3)
                        to_image.save(os.path.join(save_path, img + '_hehin' + '.jpg'))  # 保存新图
                    # if count % 2 == 0:
                    # 	print(count / 2)
                    # 	to_image.save(os.path.join(save_path, img + '_hehin' + '.jpg'))  # 保存新图
                except:
                    break


# IMAGES_PATH = r'G:\自制测试集\1208\keep\\'  # 图片集地址


IMAGES_PATH = r'G:\数据\atls\样本图片\test'  # 图片集地址
IMAGES_FORMAT = ['.jpg', '.JPG']
IMAGE_ROW = 2  # 图片间隔，也就是合并成一张图后，一共有几行
IMAGE_COLUMN = 3  # 图片间隔，也就是合并成一张图后，一共有几列


def mkd(path):
    fin_path = path + '\\' + 'hebin'
    if not os.path.exists(fin_path):
        os.mkdir(fin_path)
        return fin_path  # 图片转换后的地址
    else:
        return fin_path


def count_files(rootDir):
    for root, dirs, files in os.walk(rootDir):
        if files != []:
            image_names = [name for name in os.listdir(root)
                           for item in IMAGES_FORMAT if os.path.splitext(name)[1] == item]
            hebin_path = mkd(root)
            image_compose(image_names, hebin_path, root)
        for d in dirs:
            count_files(d)


count_files(IMAGES_PATH)
