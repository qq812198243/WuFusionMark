import os
from openai import OpenAI
from draw_objects import ImageAnnotator
import requests,json
import re


# 示例用法
if __name__ == "__main__":
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key="",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        
    )
    imgUrl = "https://bailian-bmp-prod.oss-cn-beijing.aliyuncs.com/model_offline_result/10975111/1743305380363/qianwen/IMG_20240623_135422.jpg?Expires=1743315311&OSSAccessKeyId=STS.NWgwccx4bhTfZrk9P1Aeo8sqb&Signature=oYIL7QlJCTCS1GoewUgzByrO9mE%3D&security-token=CAIS2AJ1q6Ft5B2yfSjIr5TSPNnXletD35aNWFTa3VBkTepD17bagDz2IHhMenRoAu8fv%2FU1nmlQ6%2FsZlrp6SJtIXleCZtF94oxN9h2gb4fb4yZAI22y0s%2FLI3OaLjKm9u2wCryLYbGwU%2FOpbE%2B%2B5U0X6LDmdDKkckW4OJmS8%2FBOZcgWWQ%2FKBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO%2Fks0CD0w2rlLFL%2BdugcsT4MvMBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs%2B02c5onDXgEKvEzXYrCOq4UycVRjE6IgHKdIt%2FP7jfA9sOHVnITywgxOePlRWjjRQ5ql0E4ehBQP3yBTn9%2FVTJeturjnXvGd24gk02ARqVYBMhytfsq8tbjo7uXGa%2FbB1hmjSUyYUMumi%2BluDkYtlgzV9eKArlL3Sa2Rv068HRxlNCtAXxqAAWpLDgYSuL454kMVWDk223dFiUXk5Ne8nyROa17k4VNVD0MUVR8f8eRIuj0%2FW7etng1Z3TpSboEXTShTzO4VrfX2JNO2L6pr4HgPyH9uySiGeBxiggcWyx0xHHO5Zae6w5aBpMhl5w9Jxtw7SeH3lnNrKpPcmW%2BmuqCf1u3wtHKpIAA%3D"
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

    # 输入JSON数据
    # input_json = """
    # {
    #     "image_width": 812,
    #     "image_height": 1200,
    #     "objects": [
    #         {
    #             "bbox_2d": [73, 58, 354, 206],
    #             "label": "粉色条纹伞"
    #         },
    #         {
    #             "bbox_2d": [71, 269, 354, 529],
    #             "label": "粉色云朵形状的装饰物"
    #         },
    #         {
    #             "bbox_2d": [99, 552, 517, 946],
    #             "label": "粉色卡通熊形状的装饰物"
    #         },
    #         {
    #             "bbox_2d": [476, 0, 812, 510],
    #             "label": "巨大的粉色兔子形状的装饰物"
    #         },
    #         {
    #             "bbox_2d": [525, 685, 595, 952],
    #             "label": "粉色兔子尾巴形状的装饰物"
    #         }
    #     ]
    # }
    # """
    
    # 创建标注器实例
    annotator = ImageAnnotator(result, "temporary.jpg")
    
    # 加载图片
    annotator.load_image()
    
    # 绘制标注
    annotator.draw_annotations()
    
    # 显示结果
    annotator.show_result()
    
    # 保存结果
    annotator.save_result()