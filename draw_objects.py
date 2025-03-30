import cv2
import numpy as np
import json
from PIL import Image, ImageDraw, ImageFont

class ImageAnnotator:
    def __init__(self, json_data=None, image_path=None):
        """
        初始化标注器
        :param json_data: JSON格式的标注数据
        :param image_path: 图片路径
        """
        self.json_data = json_data
        self.image_path = image_path
        self.image = None
        self.font_path = "simsun.ttc"
        
    def load_image(self, image_path=None):
        """
        加载图片
        :param image_path: 图片路径，如果不指定则使用初始化时的路径
        """
        if image_path:
            self.image_path = image_path
        self.image = cv2.imread(self.image_path)
        
    def resize_image(self, width, height):
        """
        调整图片尺寸
        :param width: 目标宽度
        :param height: 目标高度
        """
        if self.image is not None:
            self.image = cv2.resize(self.image, (width, height))
        
    def draw_annotations(self, json_data=None):
        """
        绘制标注框和标签
        :param json_data: JSON格式的标注数据，如果不指定则使用初始化时的数据
        """
        if json_data:
            self.json_data = json_data
        
        data = json.loads(self.json_data) if isinstance(self.json_data, str) else self.json_data
        
        if self.image.shape[1] != data["image_width"] or self.image.shape[0] != data["image_height"]:
            self.resize_image(data["image_width"], data["image_height"])
        
        for obj in data["objects"]:
            x1, y1, x2, y2 = obj["bbox_2d"]
            label = obj["label"]
            
            # 绘制矩形框
            cv2.rectangle(self.image, (x1, y1), (x2, y2), (255, 105, 180), 2)
            
            # 使用Pillow绘制中文文本
            pil_image = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(pil_image)
            font_size = int(data["image_height"] * 0.02)
            font = ImageFont.truetype(self.font_path, font_size)
            
            # 绘制更粗的白色描边
            offset = int(font_size * 0)
            draw.text((x1-offset, y1-font_size-offset), label, font=font, fill=(255,255,255))
            draw.text((x1+offset, y1-font_size-offset), label, font=font, fill=(255,255,255))
            draw.text((x1-offset, y1-font_size+offset), label, font=font, fill=(255,255,255))
            draw.text((x1+offset, y1-font_size+offset), label, font=font, fill=(255,255,255))
            
            # 绘制更醒目的洋红色主体文字
            draw.text((x1, y1 - font_size), label, font=font, fill=(255, 0, 255))
            self.image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    def show_result(self):
        """显示标注结果"""
        cv2.imshow("Objects", self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    def save_result(self, output_path=None):
        """
        保存标注结果
        :param output_path: 输出路径，如果不指定则使用输入图片路径加_annotated后缀
        """
        if not output_path:
            output_path = self.image_path.replace('.', '_annotated.')
        cv2.imwrite(output_path, self.image)
        print(f"标注后的图片已保存为: {output_path}")
        return output_path

# # 示例用法
# if __name__ == "__main__":
#     # 输入JSON数据
#     input_json = """
#     {
#         "image_width": 812,
#         "image_height": 1200,
#         "objects": [
#             {
#                 "bbox_2d": [73, 58, 354, 206],
#                 "label": "粉色条纹伞"
#             },
#             {
#                 "bbox_2d": [71, 269, 354, 529],
#                 "label": "粉色云朵形状的装饰物"
#             },
#             {
#                 "bbox_2d": [99, 552, 517, 946],
#                 "label": "粉色卡通熊形状的装饰物"
#             },
#             {
#                 "bbox_2d": [476, 0, 812, 510],
#                 "label": "巨大的粉色兔子形状的装饰物"
#             },
#             {
#                 "bbox_2d": [525, 685, 595, 952],
#                 "label": "粉色兔子尾巴形状的装饰物"
#             }
#         ]
#     }
#     """
    
#     # 创建标注器实例
#     annotator = ImageAnnotator(input_json, "IMG_20240623_135422.jpg")
    
#     # 加载图片
#     annotator.load_image()
    
#     # 绘制标注
#     annotator.draw_annotations()
    
#     # 显示结果
#     annotator.show_result()
    
#     # 保存结果
#     annotator.save_result()