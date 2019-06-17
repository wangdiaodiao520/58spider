import time
import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk
import tkinter.scrolledtext
import tkinter.font as tkFont
from queue import LifoQueue,Queue
import threading
from cityall import *
from crawler import *
from settings import *
import csv
from parse import *

q_url = Queue()
q_data = LifoQueue()
global q_data_point
q_data_point = 'run'

def get_time_now_str():
    '''
    获取本地时间
    :return:    datetime转为str   1900-12-31 23:59:59
    '''
    return str(time.strftime('%Y{y}%m{m}%d{d}%H{h}%M{f}%S{s}').format(y='年',m='月',d='日',h='时',f='分',s='秒'))



class ApplicationFrame(tk.Frame):
    '''
    ApplicationFrame 就是整个界面框架，填充满整个上级组件，也就是root
    show_frame 搜索结果显示框
    search_frame
    button_frame
    status_frame
    '''
    def __init__(self, master=None, title=None):
        super().__init__(master)
        master.geometry("720x480")
        master.minsize(720, 480)
        self.ft = tkFont.Font(family='微软雅黑', size=10, weight='bold')  # 创建字体
        self.show_tree_title = title
        self.gui_init(master)
        # self.gui_init_with_ttk_PanedWindow(master)


    def gui_init(self, master):
        '''
        初始化GUI组件
        '''
        # 设置顶级窗体的行列权重，否则子组件的拉伸不会填充整个窗体
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)

        # 设置继承类ApplicationFrame的grid布局位置，并向四个方向拉伸以填充顶级窗体
        self.grid(row=0, column=0, sticky=tk.NSEW)
        # 设置继承类ApplicationFrame的行列权重，保证内建子组件会拉伸填充
        self.columnconfigure(0, weight=1)

        # 第1行 创建搜索结果显示框
        row_num = 0
        self.show_frame = ttk.Frame(self)
        self.show_tree = self.init_show_frame(self.show_frame, self.show_tree_title)  # 初始化结果显示框架
        self.tree_num = 0  # 结果显示序号
        self.tree_cnt = 0  # 结果总个数
        self.show_frame.grid(row=row_num, column=0, sticky=tk.NSEW)
        self.show_frame.grid_propagate(0)
        self.rowconfigure(row_num, weight=3)

        # 第2行 创建搜索栏
        row_num += 1
        self.search_frame = ttk.Frame(self)
        self.search_var = self.init_search_frame(self.search_frame)  # 初始化搜索栏
        # self.search_frame.grid(row=row_num, column=0, sticky=tk.NSEW)
        self.search_frame.grid(row=row_num, column=0, sticky=tk.NSEW, pady=5)
        self.rowconfigure(row_num, weight=0)    # 不拉伸


        # 第3行 创建按钮栏
        row_num += 1
        self.button_frame = ttk.Frame(self)
        self.init_button_frame(self.button_frame)  # 初始化搜索栏
        self.button_frame.grid(row=row_num, column=0, sticky=tk.NSEW)
        self.rowconfigure(row_num, weight=0)    # 不拉伸

        # 第4行 创建状态栏
        row_num += 1
        self.status = tkinter.StringVar()
        self.status.set('请输入单个或多个城市名，多个城市名请用英文逗号分隔')
        label = tk.Label(self, textvariable=self.status, font=self.ft)
        label.grid(row=row_num, column=0, sticky=tk.NSEW)
        self.rowconfigure(row_num, weight=0)    # 不拉伸

        # 第5行 创建信息栏
        row_num += 1
        self.info = tk.scrolledtext.ScrolledText(self, height=6, wrap=tkinter.WORD)
        self.info.grid(row=row_num, column=0, sticky=tk.NSEW)
        self.info.configure(state='disabled')
        self.rowconfigure(row_num, weight=0)  # 权重1


    def init_control_frame(self, master):
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)

        # 第1行 创建搜索框
        search_frame = ttk.Frame(master, padding=0)
        search_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.entry_var = self.init_search_frame(search_frame)  # 初始化搜索框

        # 第2行 创建按钮框
        button_frame = ttk.Frame(master, padding=0)
        button_frame.grid(row=1, column=0, sticky=tk.NSEW)
        self.init_button_frame(button_frame)  # 初始化搜索框
    def init_show_frame(self, master, title):      # 结果表格显示
        # 分配主框架权重
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)

        # 创建表格 设置标题
        show_tree = ttk.Treeview(master, selectmode='browse', columns=title)
        # show_tree = ttk.Treeview(master, selectmode='browse')
        # show_tree = ttk.Treeview(master, height=18, selectmode='browse', columns=title)
        show_tree.grid(row=0, column=0, sticky=tk.NSEW)
        show_tree.column('#0', width=60, stretch=0)
        for i in range(len(title)):
            show_tree.heading(i, text=title[i])
            show_tree.column(i, width=80, stretch=0)
        show_tree.column(1, width=120, stretch=0)
        show_tree.column(2, width=120)
        show_tree.column(3, width=120)
        show_tree.column(12, width=120)
        show_tree.column(13, width=120)
        show_tree.column(15, width=120)

        # 设置表格框架滚动
        tree_vbar = ttk.Scrollbar(master, orient='vertical', command=show_tree.yview)
        tree_vbar.grid(row=0, column=1, sticky=tk.NS)
        tree_sbar = ttk.Scrollbar(master, orient='horizontal', command=show_tree.xview)
        tree_sbar.grid(row=1, column=0, sticky=tk.EW)
        show_tree.configure(yscroll=tree_vbar.set, xscroll=tree_sbar.set)

        return show_tree

    def init_search_frame(self, master):
        # 分配主框架权重
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=0)
        master.columnconfigure(1, weight=7)

        # 输入框
        label = tk.Label(master, text='  请输入城市地址：')
        label.grid(row=0, column=0, sticky=tk.EW)
        entry_var = tk.StringVar()
        entry = tk.Entry(master, textvariable=entry_var)
        entry.grid(row=0, column=1, sticky=tk.EW)

        label_p = tk.Label(master, text='  请输入采集页数：')
        label_p.grid(row=0, column=2, sticky=tk.EW)
        page = tk.StringVar()
        page = tk.Entry(master, textvariable=page)
        page.grid(row=0, column=3, sticky=tk.EW)

        cmb = ttk.Combobox(master)
        cmb.grid(row=0, column=4, sticky=tk.EW)
        cmb['value'] = ('二手房','个人二手房')
        cmb.current(0)

        return entry_var,page,cmb


    def init_button_frame(self, master):
        # 分配主框架权重
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)

        # 按钮
        b1 = tk.Button(master, text='开始', command=lambda:self.thread_it(self.start))
        b1.grid(row=0, column=0, sticky=tk.EW)

        b2 = tk.Button(master, text='停止', command=self.stop)
        b2.grid(row=0, column=1, sticky=tk.EW)

    def get_search_content(self):
        return self.search_var.get()

    def set_select_info(self, str):
        self.select_label.config(text=str)

    def set_status(self, str):      # 显示状态栏信息
        if str:
            self.status.set(str)


    def insert_info(self, s: str):  # 信息栏增加信息
        if s:
            t = get_time_now_str()
            self.info.configure(state='normal')
            self.info.insert(tkinter.END, t + ' ' + s + '\n')
            self.info.yview_moveto(1)
            self.info.configure(state='disabled')

    def insert_tree(self, item):    #  结果表格添加数据 ['xxx',...]格式
        '''
        结果表格添加数据
        :param item:    结果数据，['xxx',...]格式
        '''
        if item:
            self.tree_num += 1
            self.tree_cnt += 1
            self.show_tree.insert('', self.tree_num, text=str(self.tree_num), values=item)
            self.show_tree.yview_moveto(1)

            if self.tree_cnt > 100:     # 保持100条记录
                cnt = 0
                items = self.show_tree.get_children()
                # print(items)
                for item in items:
                    self.show_tree.delete(item)
                    self.tree_cnt -= 1
                    cnt += 1
                    if cnt >= 30:
                        break


    def stop(self):
        global q_data_point
        q_data_point = 'stop'


    def start(self):
        global q_data_point
        q_data_point = 'run'
        point = self.search_var[2].get()
        if point == "二手房":
            list_offset_url = ESF_M_LIST
            data_offset_url = ESF_M_DATA
        elif point == "个人二手房":
            list_offset_url = ESF_P_M_LIST
            data_offset_url = ESF_P_DATA
        else:
            pass
        page = self.search_var[1].get()
        city_input = self.search_var[0].get()
        self.insert_info('识别城市信息：' + city_input )
        city_input = city_input.split(',')
        for citys in city_input:
            self.set_status('正在采集' + citys + '信息')
            self.insert_info('开始采集' + citys + '市信息')
            path = citys + '_' + point + '_' + get_time_now_str() + '.csv'
            with open(path, 'a', newline='', encoding='gbk') as f:  # 写入字段头
                write = csv.writer(f, dialect='excel')
                write.writerow(["名称", "小区", "地址", "联系人", "联系电话", "所属公司", "售价", "产权", "户型", "面积", "楼层", "朝向", "类型", "装修", "建筑年代", "发布时间"])
            citys = citylist[citys]
            urls = [list_offset_url.format(city=citys, num=i) for i in range(int(page))]
            for url in urls:
                Crawler(url, q_url, q_data).get_normal()
                data_urls = [data_offset_url.format(city=citys, bm=q_url.get()) for _ in range(q_url.qsize())]
                for i in data_urls:
                    if q_data_point == 'run':
                        res = Crawler(i, q_url, q_data).get_normal()
                        if type(res).__name__ == 'str':
                            if '验证' in res:
                                self.set_status('出现手势验证码，请手动打开网页并验证')
                                self.insert_info('断点网址为：'+ i)
                                exit()
                            else:
                                pass
                        else:
                            pass
                        try:
                            if '*' in res['phone'] and point == "二手房":
                                time.sleep(1)
                                PHONE_URL = i.replace('/'+citys,'').replace('m.',citys+'.')
                                res['phone'] = get_phone(PHONE_URL)
                            else:
                                pass
                            data = list(res.values())
                            self.insert_tree(data)
                            with open(path, 'a', newline='', encoding='gbk') as f:  # 写入采集结果
                                write = csv.writer(f, dialect='excel')
                                write.writerow(data)
                        except:
                            pass
                    else:
                        self.set_status('终止程序')
                        exit()
                    time.sleep(1)
        self.set_status('采集完成')
        self.insert_info('采集完成')





    # 方法线程，防止gui界面卡死
    @staticmethod
    def thread_it(func):
        t = threading.Thread(target=func)
        t.start()




def main():
    master = tk.Tk()
    app_ui_tree_title = ("名称", "小区", "地址", "联系人", "联系电话", "所属公司", "售价", "产权", "户型", "面积", "楼层",
                         "朝向", "类型", "装修", "建筑年代", "发布时间")
    gui = ApplicationFrame(master,app_ui_tree_title)
    gui.mainloop()

if __name__ == '__main__':

    main()
