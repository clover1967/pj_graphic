from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

#-----------
# 变量初始化
#-----------

g_fViewDistance = 9.    # 观察点的z轴坐标
g_Width = 600           # 窗口宽度
g_Height = 600          # 窗口高度

g_nearPlane = 1.        # 观察点到近截面的距离
g_farPlane = 100.      # 观察点到远截面的距离

action = ""             # 记录鼠标和键盘的动作的字符串，被声明为全局变量
xStart = yStart = 0.    # 运行过程中记录鼠标在窗口中的起始位置，以此将鼠标的动作转化成对图像的变换
zoom = 45.              # 观察点相对y轴的角度，以度数计

xRotate = 0.            # x轴方向上的旋转偏移量
yRotate = 0.            # y轴方向上的旋转偏移量
zRotate = 0.            # z轴方向上的旋转偏移量

xTrans = 0.             # x轴方向上的平移偏移量
yTrans = 0.             # y轴方向上的平移偏移量

#-------------------
# 构建含有一个茶壶的场景
#-------------------

def scenemodel():
    glRotate(90, 0., 0., 1.)
    glutSolidTeapot(1.)

def printHelp(): 
    print ("""\n
         -------------------------------------------------------------------\n
         鼠标左键                - 旋转物体(+Shift键只在z轴上旋转)\n
         鼠标中键                - 移动物体\n
         鼠标右键                - 放大/缩小物体\n
         键盘R键                 - 重置视图\n
         键盘Q键                 - 退出程序\n
         -------------------------------------------------------------------\n
         \n""")

def init():                             # 初始化光源、深度、阴影等
    glEnable(GL_NORMALIZE)
    glLightfv(GL_LIGHT0, GL_POSITION, [.0, 10.0, 10., 0.])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [.0, .0, .0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glShadeModel(GL_SMOOTH)
    resetView()

def display():
    # 清空颜色缓冲和深度缓冲
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # 设置观察点的位置，这里设置为从-z轴观察
    glLoadIdentity()
    gluLookAt(0, 0, -g_fViewDistance, 0, 0, 0, -.1, 0, 0)
    # 设置视角
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(zoom, float(g_Width) / float(g_Height), g_nearPlane, g_farPlane)
    glMatrixMode(GL_MODELVIEW)
    # 生成图像
    polarView()
    scenemodel()
    glutSwapBuffers()

def reshape(width, height):             # 设置观察窗口的大小
    global g_Width, g_Height
    g_Width = width
    g_Height = height
    glViewport(0, 0, g_Width, g_Height)

def resetView():                        # 该函数将视图重置为初始状态
    global zoom, xRotate, yRotate, zRotate, xTrans, yTrans
    zoom = 65.
    xRotate = 0.
    yRotate = 0.
    zRotate = 0.
    xTrans = 0.
    yTrans = 0.
    glutPostRedisplay()

def polarView():                        # 应用平移、旋转的偏移量
    glTranslatef(yTrans / 100., 0.0, 0.0 )
    glTranslatef(0.0, -xTrans / 100., 0.0)
    glRotatef(-zRotate, 0.0, 0.0, 1.0)
    glRotatef(-xRotate, 1.0, 0.0, 0.0)
    glRotatef(-yRotate, .0, 1.0, 0.0)

def keyboard(bkey, x, y):               # 定义键盘操作，这里的参数x，y是为了符合glutKeyboardFunc的接口定义，mouse()函数中的state参数同
    key = bkey.decode('utf-8')
    if(key == 'r'):
        resetView()
    if(key == 'q'):
        exit(0)
    glutPostRedisplay()

def mouse(button, state, x, y):         # 定义鼠标操作
    global action, xStart, yStart
    if (button == GLUT_LEFT_BUTTON):
        if (glutGetModifiers() == GLUT_ACTIVE_SHIFT):
            action = "MOVE_EYE_2"       # 只在z轴旋转，旋转由鼠标上下移动控制
        else:
            action = "MOVE_EYE"         # 在x轴和y轴两个方向上都旋转
    elif (button == GLUT_MIDDLE_BUTTON):
        action = "TRANS"                # 平移
    elif (button == GLUT_RIGHT_BUTTON):
        action = "ZOOM"                 # 放大或缩小
    # 更新光标起始位置
    xStart = x
    yStart = y

def motion(x, y):                       # 根据鼠标动作的类型和鼠标位置的变化计算相应的偏移量，并更新图像
    # x，y为新的光标位置; xStart，yStart为动作前光标的起始位置
    global zoom, xStart, yStart, xRotate, yRotate, zRotate, xTrans, yTrans
    if (action == "MOVE_EYE"):
        xRotate += x - xStart
        yRotate -= y - yStart
    elif (action == "MOVE_EYE_2"):
        zRotate += y - yStart
    elif (action == "TRANS"):
        xTrans += x - xStart
        yTrans += y - yStart
    elif (action == "ZOOM"):
        zoom -= y - yStart
        if zoom > 150.:
            zoom = 150.
        elif zoom < 1.:
            zoom = 1.
    else:
        print("unknown action\n", action)
    xStart = x
    yStart = y
    glutPostRedisplay()             # 计算出动作的偏移量后，标志当前窗口需要重新绘图

if __name__ == "__main__":
    # glut窗口初始化
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(g_Width, g_Height) 
    glutCreateWindow("Teapot")
    # 调用自定义的Init()函数初始化
    init()
    # 将自定义的重置图像、展示、鼠标操作、键盘操作、图像动作函数关联到glut对应的接口，以供主循环调用
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)    
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutKeyboardFunc(keyboard)

    printHelp()
    # 将控制流移交到glut主循环
    glutMainLoop()