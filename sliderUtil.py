#  滑动滑块的两个关键点为：（1）生成滑动轨迹（2）控制滑动按钮进行滑动
# （1）根据要滑动的距离生成滑动轨迹，此处是模拟人为滑动：先加速滑动滑块，再减速滑动滑块。代码如下：
# 其中distance参数就是要滑动的距离，返回值tracks为生成的滑动轨迹,，后面要把tracks传给滑动滑块的函数。
import time

from selenium.webdriver import ActionChains


def get_tracks(distance):
    """
    根据偏移量获取移动轨迹
    :param distance:偏移量
    :return:移动轨迹
    """
    # 移动轨迹
    tracks = []
    # 当前位移
    current = 0
    # 减速阈值
    mid = int(distance * 4 / 5)
    # 计算间隔
    t = 0.2
    # 初速度
    v = 0
    while current < distance:
        if current < mid:
            # 加速度为正2
            a = 5
        else:
            # 加速度为负3
            a = -3
        # 初速度v0
        v0 = v
        # 当前速度
        v = v0 + a * t
        # 移动距离
        move = int(v0 * t + 1 / 2 * a * t * t)
        # 当前位移
        current += move
        # 加入轨迹
        tracks.append(round(move))
    return tracks

    # （2）控制滑动按钮进行滑动，代码如下：
    # 其中slider就是获取到的滑块按钮，tracks就是上面（1）中的函数返回的滑动轨迹。
def move_to_gap(slider, tracks, browser):
    """
        拖动滑块
        :param browser:
        :param slider: 滑块
        :param tracks: 轨迹
        :return:
        """
    # 模拟滑动滑块
    action = ActionChains(browser) # 初始化一个鼠标对象
    action.click_and_hold(slider).perform() # 鼠标按住左键不动
    for i in tracks:
        action.move_by_offset(xoffset=i, yoffset=0).perform()
        # 新建ActionChains对象防止累加位移
        action = ActionChains(browser)
    time.sleep(0.5)
    # 释放滑块
    action.release().perform()
