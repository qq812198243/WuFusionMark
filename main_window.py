from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, QGroupBox, QHBoxLayout
from PyQt5.QtCore import Qt
import sys,cv2
import os,re
import json
from draw_objects import ImageAnnotator
import requests
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from io import BytesIO
from openai import OpenAI
import random
import string
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图像标注工具")
        
        # 创建加载动画标签
        self.loading_label = QLabel(self)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: #4CAF50;
                margin: 20px;
            }
        """)
        self.loading_label.setText("加载中...")
        self.loading_label.hide()
        self.setGeometry(100, 100, 800, 600)
        
        # 创建主部件和布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        
        # 第一区域：输入设置
        input_group = QGroupBox("输入设置")
        input_layout = QVBoxLayout()
        # 新增用于输入网络图片URL的输入框
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("请输入网络图片URL")
        input_layout.addWidget(self.url_input)

        # 新增预览按钮，点击后预览输入的网络图片
        self.preview_button = QPushButton("预览网络图片")
        self.preview_button.clicked.connect(self.preview_network_image)
        input_layout.addWidget(self.preview_button)
        self.img_dir_input = QLineEdit()
        self.img_dir_input.setPlaceholderText("请输入图片文件夹路径")
        input_layout.addWidget(self.img_dir_input)
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("请输入API密钥")
        input_layout.addWidget(self.api_key_input)
        
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)
        
        # 第二区域：预览区域
        preview_group = QGroupBox("预览")
        preview_layout = QHBoxLayout()
        
        self.original_preview = QLabel("原始图片预览")
        self.original_preview.setAlignment(Qt.AlignCenter)
        preview_layout.addWidget(self.original_preview)
        
        self.annotated_preview = QLabel("标注效果预览")
        self.annotated_preview.setAlignment(Qt.AlignCenter)
        preview_layout.addWidget(self.annotated_preview)
        
        preview_group.setLayout(preview_layout)
        main_layout.addWidget(preview_group)
        
        # 第三区域：操作按钮
        button_group = QGroupBox()
        button_layout = QHBoxLayout()
        
        self.button = QPushButton("开始标注")
        self.button.clicked.connect(self.start_annotation)
        button_layout.addWidget(self.button)
        
        button_group.setLayout(button_layout)
        main_layout.addWidget(button_group)
        
        # 应用样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 18px;
                color: #333;
                margin: 20px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                margin: 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
    
    def preview_network_image(self):
        """预览网络图片"""
        url = self.url_input.text().strip()
        if not url:
            self.original_preview.setText("请输入有效的图片URL")
            return
            
        try:
            # 这里添加下载网络图片并显示的代码
            self.original_preview.setText("正在加载网络图片...")
            # 实际实现需要添加网络请求和图片处理逻辑


            try:
                response = requests.get(url)
                response.raise_for_status()
                img_data = response.content
                img = QImage.fromData(img_data)
                if not img.isNull():
                    pixmap = QPixmap.fromImage(img)
                    scaled_pixmap = pixmap.scaled(self.original_preview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.original_preview.setPixmap(scaled_pixmap)
                else:
                    self.original_preview.setText("无法加载图片，请检查URL或图片格式")
            except requests.RequestException as e:
                self.original_preview.setText(f"加载网络图片失败: {str(e)}")
        except Exception as e:
            self.original_preview.setText(f"加载网络图片失败: {str(e)}")
    
    def start_annotation(self):
        api_key = self.api_key_input.text().strip()
        if not api_key:
            self.original_preview.setText("请输入有效的API密钥")
            return
            
        self.original_preview.setText("正在处理图片...")
        
        # 确保img文件夹存在
        img_dir = os.path.join(os.path.dirname(__file__), self.img_dir_input.text().strip())
        if not os.path.exists(img_dir):
            self.original_preview.setText(f"img文件夹不存在: {img_dir}")
            return
            
        client = OpenAI(
            # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
            api_key= self.api_key_input.text().strip(),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            
        )
        imgUrl = self.url_input.text().strip()
        prompt = """
        输出分辨率时不要让原始图片变形比例要对
        请按照以下json格式输出：
        ```json
        {
        “image_width”: ,
        ”image_height“: ,
        “resolution”[],
        “objects”: [
            {
                ”bbox_2d“: [],
                “label”:""
            }
        ]
        }
        ```

        """

        completion = client.chat.completions.create(
            temperature=0.7,
            top_p=0.9,
            model="qwen-vl-max-latest",  # 此处以qwen-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=[{"role": "user","content": [
                    {"type": "text","text": prompt},
                    {"type": "image_url",
                    "image_url": {"url": imgUrl}}
                    ]}]
            )
        # 显示加载动画
        self.original_preview.setText("正在处理图片...")
        self.loading_label.show()
        
        # 下载图片
        response = requests.get(imgUrl)
        print("completion:", completion.model_dump_json())

        result = completion.choices[0].message.content
        print("API返回内容:", result)


        if response.status_code == 200:
            temp_image_path = "temporary.jpg"
            with open(temp_image_path, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
        
        try:

            # 使用正则表达式提取 ```json ``` 中间的值
            pattern = r'```json\s*([\s\S]*?)\s*```'
            match = re.search(pattern, result)

            if match:
                json_content = match.group(1)
                print("提取的JSON内容:", json_content)
                # 尝试解析JSON
                result=json.loads(json_content)
            else:
                print("未找到符合条件的JSON内容")
                # 尝试解析JSON
                result=json.loads(result)
                print("JSON格式验证通过")
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            print("API返回的不是有效的JSON格式")
            # 创建标注器实例
        annotator = ImageAnnotator(result, "temporary.jpg")
        
        # 加载图片
        annotator.load_image()
        
        # 绘制标注
        annotator.draw_annotations()
        
        # 显示结果
        annotator.show_result()
        
        # 将标注后的图片显示在预览区域
        annotated_image = cv2.cvtColor(annotator.image, cv2.COLOR_BGR2RGB)
        height, width, channel = annotated_image.shape
        bytes_per_line = 3 * width
        q_img = QImage(annotated_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        scaled_pixmap = pixmap.scaled(self.annotated_preview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.annotated_preview.setPixmap(scaled_pixmap)
        
        # 隐藏加载动画
        self.loading_label.hide()
        
        # 生成随机文件名
        random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        new_filename = f"{random_chars}.jpg"
        img_dir = os.path.join(img_dir, new_filename)
        # 保存结果
        annotator.save_result(output_path=img_dir)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())