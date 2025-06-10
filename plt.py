# 导入需要的库
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.font_manager as fm
import os

# --- 自动查找可用的中文字体 ---
def find_chinese_font():
    """
    在一个列表中按顺序查找系统中可用的中文字体。
    """
    # 包含了常见的几种中文字体，你可以根据需要添加
    font_names = [
        'WenQuanYi Zen Hei', # 文泉驿正黑，推荐在 Linux 下安装
        'SimHei',            # 黑体
        'Microsoft YaHei',   # 微软雅黑
        'Heiti TC',          # 黑体-繁
    ]
    
    # 获取系统上所有可用字体的列表
    all_font_names = {font.name for font in fm.fontManager.ttflist}
    
    for font_name in font_names:
        if font_name in all_font_names:
            # 找到了，立即返回字体名称
            print(f"✅ 成功找到可用的中文字体: {font_name}")
            return font_name
            
    # 如果循环结束了还没找到
    return None

# --- 主绘图逻辑 ---

# CSV 文件名
csv_file = "results.csv"

# 检查 CSV 文件是否存在
if not os.path.exists(csv_file):
    print(f"错误: {csv_file} 文件未找到。请先确保实验脚本单元格已经成功运行。")
else:
    # 从 CSV 文件读取实验数据
    df = pd.read_csv(csv_file)

    # 尝试设置中文字体
    chinese_font = find_chinese_font()
    if chinese_font:
        plt.rcParams['font.sans-serif'] = [chinese_font] # 设置字体
        plt.rcParams['axes.unicode_minus'] = False      # 解决负号显示为方框的问题
    else:
        # 如果找不到任何中文字体，打印警告信息
        print("⚠️ 警告: 未在系统中找到可用的中文字体。")
        print("图表中的中文将无法正常显示，建议按照之前的说明安装字体（如 `sudo apt-get install -y fonts-wqy-zenhei`）。")

    # --- 开始绘图 ---
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7))

    # 绘制折线图
    ax.plot(df['block_size_kb'], df['throughput_gb_s'], marker='o', linestyle='-')

    # 设置图表标题和坐标轴标签
    ax.set_title('系统 I/O 吞吐量 vs. 缓冲区大小', fontsize=16)
    ax.set_xlabel('缓冲区大小 (KB) - 对数刻度', fontsize=12)
    ax.set_ylabel('吞吐量 (GB/s)', fontsize=12)

    # X轴使用以2为底的对数刻度
    ax.set_xscale('log', base=2)
    ax.set_xticks(df['block_size_kb'])
    ax.get_xaxis().set_major_formatter(mticker.ScalarFormatter())
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    # 在 Jupyter Notebook 中，plt.show() 会直接显示图表
    plt.show()