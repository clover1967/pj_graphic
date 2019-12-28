## 计算机图形学PJ报告

<p align="right">吴钟立 15307130213</p>

### PJ1

环境：python3 + pydub + matplotlib + numpy

实现方法：使用pydub将mp3文件转为wav文件，用matplotlib绘制时域波形图和频域成分图，通过调用plot.ion()  设置绘图为交互式，每隔一个短的时间间隔便刷新图像，每帧图像对应一个窗口长度的采样点，以此实现音频动态显示的效果

运行：`python3 audio_visualization.py filename.mp3`

### PJ2

环境：python3 + pyOpenGL

实现方法：调用pyOpenGL的接口，画一个茶壶，并通过读取鼠标和键盘动作修改显示的坐标和偏移量、观察角度等参数，实现对物体的平移、旋转、放大/缩小功能

运行：`python3 teapot.py`(要退出程序，请单击图像窗口左下角的exit按钮)

### PJ3

实现方法：用adobe animate绘制了一个含有20个关键帧、帧率为30fps的火柴人扣篮动画