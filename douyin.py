# 滑块验证码处理
# 1. web 自动化显示验证码
# 2. 获取滑块以及滑块图片地址
# 3. 下载滑块以及滑块图片
# 4. 人工智能匹配滑块验证码距离
# 5. 缩放比例以及校准滑块偏移量
# 6. ActionChanis滑块解锁
# 7. 人工智能模拟和跟踪滑块滑动轨迹
# 8. 滑动失败后增加重试机制
# 1. web 自动化显示验证码
import time
from http.cookiejar import LWPCookieJar
import cv2
import requests as requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image as image
import sliderUtil
import Cookie
import json

# session = Cookie.dylogin()
base_url = 'https://www.douyin.com/search/云南?source=search_history&type=user'
driver = webdriver.Chrome()
# 滑块验证登录
while True:
    driver.get(base_url)
    time.sleep(2)
    # 2. 获取滑块以及滑块图片地址
    big_ele = driver.find_element(By.XPATH, '//*[@id="captcha-verify-image"]')
    big_url = big_ele.get_attribute('src')
    print("big_url:" + big_url)
    small_ele = driver.find_element(By.XPATH, '//*[@id="captcha_container"]/div/div[2]/img[2]')
    small_url = small_ele.get_attribute('src')
    print('small_url:' + small_url)
    # 3. 下载滑块以及滑块图片
    with open('img/big_img.jpeg', 'wb') as f:
        f.write(requests.get(big_url).content)
        f.close()
    with open('img/small_img.png', 'wb') as f:
        f.write(requests.get(small_url).content)
        f.close()
        # 4. 人工智能匹配滑块验证码距离
        big_gray = cv2.imread('img/big_img.jpeg', 0)  # 以灰度模式加载图片
        small_gray = cv2.imread('img/small_img.png', 0)  # 以灰度模式加载图片
        # 大图灰色模版和小图灰色模版比较
        res = cv2.matchTemplate(big_gray, small_gray, cv2.TM_CCORR_NORMED)  # 匹配对象
        distance = cv2.minMaxLoc(res)  # 匹配小图和大图最左边和最右边的结果
        print(distance)

        # 获取原图像素
        big_img_size = image.open('img/big_img.jpeg')
        big_w = big_img_size.width  # 原图的宽
        big_h = big_img_size.height  # 原图的高

        # 5. 缩放比例以及校准滑块偏移量    实际 340*212  原图   big_w * big_h
        x = distance[2][0]  # 原图距离
        # print(x)  # x+5 = big_w
        x = int(x * 340 / big_w)  # 缩放比例
        # print(x)
        py = 5 - int(5 * 340 / big_w)  # 偏移量
        # print(py)
        x = x - py  # 滑块的移动距离
        # print(x)
        # 6. ActionChanis滑块解锁
        small_ele = driver.find_element(By.XPATH, '//*[@id="captcha_container"]/div/div[2]/img[2]')
        # action = ActionChains(driver)  # 初始化一个鼠标对象
        # action.click_and_hold(small_ele).perform()  # 鼠标按住左键不动
        # action.drag_and_drop_by_offset(small_ele, x, 0).perform()  # 把滑块滑动到指定的坐标

        # 7. 人工智能模拟和跟踪滑块滑动轨迹
        tracks = sliderUtil.get_tracks(distance=x)
        sliderUtil.move_to_gap(slider=small_ele, tracks=tracks, browser=driver)
        # 8. 滑动失败后增加重试机制
        time.sleep(2)
    try:
        driver.find_element(By.XPATH, '//*[@id="secsdk-captcha-drag-wrapper"]/div[2]')
    except Exception as e:
        break
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 页面先滑到最底端
time.sleep(3)
login_ele = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]/div[3]/div/div/span')
login_ele.click()
time.sleep(5) #用于扫码时间

#滑到底部
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(1)


