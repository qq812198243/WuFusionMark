# 图像标注工具

## 项目概述
这是一个基于Qwen-VL-Max API和OpenCV的图像标注工具，可以自动识别图片中的物体并生成标注框和标签。

## 功能特性
- 支持网络图片URL输入
- 自动识别图片中的物体并标注
- 支持标注结果预览和保存
- 提供简洁的图形用户界面

## 安装指南
```bash
pip install -r requirements.txt
```

## 使用方法
1. 运行`main_window.py`启动图形界面
2. 输入API密钥和图片URL
3. 点击"开始标注"按钮
4. 查看标注结果并保存

## 技术细节
- 使用Qwen-VL-Max API进行图像识别
- 使用OpenCV进行图像处理和标注绘制
- 使用PyQt5构建用户界面

## 示例代码
```python
# 基本使用示例
from draw_objects import ImageAnnotator

# 创建标注器实例
annotator = ImageAnnotator(json_data, "image.jpg")

# 加载并标注图片
annotator.load_image()
annotator.draw_annotations()
annotator.show_result()
annotator.save_result()
```

## 注意事项
- 需要有效的API密钥 
- 图片URL必须可公开访问
- 标注结果会保存在本地"img"文件夹中
- 官网https://bailian.console.aliyun.com/ 注册账号，创建应用，获取API密钥，然后填入代码中的`api_key`变量。

## 贡献指南
欢迎提交问题和建议，或者直接提交Pull Request。

## 许可证
MIT License

## 作者
- [allenW]
- 联系方式：qq:812198243

## 版本历史
- v1.0.0 初始版本，支持基本功能

## 代码名称
- 项目名称：多模态图像标注工具