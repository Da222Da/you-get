import gradio as gr
import subprocess
# import os
import re

def extract_streams_info(input_string):
    """
    从包含YouTube视频流信息的字符串中提取itag和quality信息。

    参数:
    input_string (str): 包含视频流信息的字符串。

    返回:
    list: 包含itag和quality信息的列表，其中每个元素都是一个字典。
    """
    # 使用正则表达式匹配所有包含itag和quality的行
    itag_quality_pattern = re.compile(r'- itag:\s+(\d+)\s+.*?quality:\s+([^\(]+)\s*\(?.*?\)?')
    
    # 创建一个空列表来存储结果
    streams = []
    
    # 查找所有匹配项
    for match in itag_quality_pattern.finditer(input_string):
        # 提取itag和quality
        itag = match.group(1)
        quality = match.group(2).strip()  # 去除可能的空白字符
        # 将它们添加到字典中，然后将字典添加到列表中
        streams.append({"itag": itag, "quality": quality})
    
    # 返回结果列表
    return streams


with gr.Blocks() as demo:
    name = gr.Textbox(label="请输入下载视频 URL：")
    output = gr.Textbox(label="视频信息解析结果：")
    create_itag_btn = gr.Button("生成视频信息 itag")

    # 使用修饰器语句，处理事件监听
    @create_itag_btn.click(inputs=name, outputs=output)
    def get_itag(url):
        try:
            command = ['you-get', '-i', url]
            result = subprocess.run(command, capture_output=True, text=True)
            print(result)
            if result.returncode == 0:
                gr.Warning("视频信息生成成功")
                streams = extract_streams_info(result.stdout)
                print(streams)
                return ""
            else:
                return "抱歉！视频信息解析失败，请自行排查原因。"
        except Exception as e:
            # 如果捕获到异常，则执行这里的代码
            print(f"捕获到异常：{e}")

if __name__ == "__main__":
    demo.launch(share=True)


# 获取视频信息
# def get_itag(url):
#     try:
#         # 定义命令和参数
#         command = ['you-get', '-i', url]

#         # 执行命令并捕获输出
#         # 注意：如果不需要捕获输出，可以省略capture_output=True参数
#         # 如果你希望同时捕获stdout和stderr，并且它们能够一起被访问，可以设置stderr=subprocess.STDOUT
#         result = subprocess.run(command, capture_output=True, text=True)
#         print(result)
#         # 检查命令是否成功执行
#         # if result.returncode == 0:
#         #    # 使用os.path.expanduser来确保~被正确处理
#         #     output_dir = os.path.expanduser(output_dir)
#         #     # subprocess.run(["you-get", "-o", output_dir, url], check=True)
#         #     streams = parse_streams(result.stdout)
#         #     highest_itag = get_highest_quality_itag(streams)
            
#         #     if highest_itag:
#         #         subprocess.run(["you-get", "-o", output_dir, '--itag', highest_itag, url])
#         # else:
#         #     # 打印标准错误
#         #     print("An error occurred:")
#         #     print(result.stderr)
       
#     except subprocess.CalledProcessError as e:
#         print(f"命令执行失败，退出码为：{e.returncode}")
#     except FileNotFoundError:
#         print("未找到you-get命令，请确保已安装you-get")
#     except Exception as e:
#         print(f"发生错误：{e}")
