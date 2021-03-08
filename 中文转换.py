import ctypes  # 用于适配DPI
import os
import pathlib
import time
import tkinter.messagebox
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *  # 用于tkinter的美化

import opencc
from windnd import windnd

'''lang_dict_sc = {
    'title': '繁简转换GUI', 'Beth': '9102', 'Cecil': '3258'
}'''

root_frame = Tk()
root_frame.iconbitmap('ji.ico')

# DPI适配
# 告诉操作系统使用程序自身的dpi适配
ctypes.windll.shcore.SetProcessDpiAwareness(1)
# 获取屏幕的缩放因子
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
# 设置程序缩放
root_frame.tk.call('tk', 'scaling', ScaleFactor / 75)

root_frame.title('繁简转换GUI')
file_frame = Frame(root_frame)
file_frame.pack(padx=10, pady=10)  # 选择文件Frame
option_frame = Frame(root_frame)
option_frame.pack(padx=10, pady=10)  # 设置Frame
action_frame = Frame(root_frame)
action_frame.pack(padx=10, pady=10)

need_to_log = IntVar()  # 是否在控制台输出
to_log_checkbox = Checkbutton(option_frame, text='输出日志到控制台',
                              onvalue=1, offvalue=0, variable=need_to_log).pack(fill=X, side=LEFT)

has_time_in_name = IntVar()  # 是否在输出名字中包含时间戳
has_time_in_name_checkbox = Checkbutton(option_frame, text='输出带时间戳',
                                        onvalue=1, offvalue=0, variable=has_time_in_name).pack(fill=X, side=LEFT)
need_to_convert_name = IntVar()  # 是否翻译名字
need_to_convert_name.set(1)
convert_name_checkbox = Checkbutton(option_frame, text='翻译文件名',
                                    onvalue=1, offvalue=0, variable=need_to_convert_name).pack(fill=X, side=LEFT)

subtitle_path = StringVar()  # 输入文件目录
file_path_entry = Entry(file_frame, width=50, textvariable=subtitle_path).pack(fill=X, side=LEFT)  # x方向填充,靠左


def drag(files: list):  # 拖拽文件功能 只识别第一个
    if need_to_log.get() == 1:
        if len(files) > 1:
            print('More than one file is dropped!')
    str_path = files[0]
    subtitle_path.set(str_path)


windnd.hook_dropfiles(root_frame, func=drag, force_unicode=True)  # 拖拽文件 范围整个GUI 必须使用Unicode 否则中文会报错


def select_a_file():
    file_selector = askopenfilename()
    if file_selector:
        subtitle_path.set(file_selector)


def t2s():
    cc_convert('t2s')


def s2t():
    cc_convert('s2t')


def cc_convert(arg: str):
    cc = opencc.OpenCC(arg)
    if subtitle_path.get() != '':  # 判断文件目录不为空
        subtitle_path_str = subtitle_path.get()
        input_file = open(subtitle_path_str, 'r', encoding='utf-8')  # 中文如果不用Unicode
        path = pathlib.Path(subtitle_path_str)
        if has_time_in_name.get() == 1:
            time_stamp = ''.join(['_', str(time.time())])
        else:
            time_stamp = ''
        if need_to_convert_name.get() == 1:
            file_name = cc.convert(path.stem)
        else:
            file_name = path.stem
        out_name = ''.join([file_name, '_', arg, time_stamp, path.suffix])  # 文件名+-TC+时间戳+后缀名
        out_file_path = os.path.join(path.parent, out_name)  # 路径+生成的文件名
        if need_to_log.get() == 1:
            print('Output path is: ')
            print(out_file_path)

        #######

        try:
            input_text = input_file.read()
        except IOError:
            input_file.close()
            tkinter.messagebox.showwarning('错误', '不能读取数据', parent=root_frame)
        except UnicodeDecodeError:
            input_file.close()
            tkinter.messagebox.showwarning('错误', '不是文本文件', parent=root_frame)
        else:
            out_file = open(out_file_path, 'w', encoding='utf-8')
            out_file.write(cc.convert(input_text))
            input_file.close()
            out_file.close()
    else:
        tkinter.messagebox.showwarning('错误', '路径为空', parent=root_frame)


open_button = Button(file_frame, width=20, text='选择文件', command=select_a_file).pack(fil=X, padx=10)
s2t_button = Button(action_frame, width=10, text='简转繁', command=s2t).pack(fill=X, side=LEFT)
t2c_button = Button(action_frame, width=10, text='繁转简', command=t2s).pack(fill=X, side=LEFT)
exit_button = Button(action_frame, width=10, text='退出', command=root_frame.quit).pack(fill=Y, padx=10)

root_frame.mainloop()
