import time
import re
from DrissionPage import ChromiumPage
from DrissionPage import ChromiumOptions
from tqdm import tqdm


def run_word():
    # 阅读文档 - 60秒
    for i in tqdm(range(60), mininterval=0.5):
        time.sleep(1)
    # time.sleep(60)


def run_video(right_box):
    # 处理开始播放时间   结束播放时间
    strat_time = re.findall('(.*):(.*)', right_box.ele('x:.//span[@class="dplayer-ptime"]').text)
    strat_time = int(strat_time[0][0]) * 60 + int(strat_time[0][1])
    end_time = re.findall('(.*):(.*)', right_box.ele('x:.//span[@class="dplayer-dtime"]').text)
    end_time = int(end_time[0][0]) * 60 + int(end_time[0][1])
    # 播放视频秒数
    video_time = end_time - strat_time

    # 点击静音
    right_box.ele('x:.//button[@class="dplayer-icon dplayer-volume-icon"]').click()

    # 点击播放按钮
    right_box.ele('x:.//button[@class="dplayer-icon dplayer-play-icon"]').click()

    # 等待播放时间
    for i in tqdm(range(video_time), mininterval=0.5):
        time.sleep(1)
    # time.sleep(video_time + 3)


def run():
    # 直接获取右边ele
    # 判断类型： 课件 or 视频
    right_box = page.ele('x:.//div[@class="video-box"]')
    is_word = right_box.ele('x:./div[@class="ifrema"]')

    # 是课件
    if is_word:
        print('识别到课件：等待60秒')
        time.sleep(0.5)
        run_word()
    else:
        print('识别到视频：点击播放')
        run_video(right_box)


# 获取详细信息
def get_detail_info(x_chapters):
    detaill_infos = x_chapters.eles('x:.//div[@class="second-level-inner-box"]/div')
    for detaill_info in detaill_infos:
        # 判断完成状态
        status_s = detaill_info.ele('x:.//div[@class="complate-icon"]//img', timeout=0.2)
        if not status_s:
            titile = detaill_info.ele('x:.//p[@class="title"]').text
            print('>', titile, '   未定义')

        # 判断状态是否为 未完成 or 完成了一半
        elif status_s.link == 'data:image/png;base64,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' or status_s.link == 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAbVJREFUSEu9ls8rRFEUx7/nzsjvjWQxSSTPJE1Zv0nUjEiIhRQbxQKTUiSr914pK6mJFWUjlqL8ysbCrJWVIWUh/wBF4R3d18w0zMwzi7nztu/7zuee7zn3nEdweQJGV/2H+BqCzf0gNAPwJeQvYDxC0EmZ7T26ta6ec4WhbC9aDd3HBIsZkwB73A4B0DcRdolhxK3Yy19tBqDV0AcZ2GNwtVd4EPJ3IuzvRLvPj7rqWnSshbPyCPRKwETcih2nC34BWszgPGBvgCFk0OWeOTTU1P8KqJl67oQINiAWHszraFKUAsiT28SHBBKLoRlM6+NZA7kC5BcEWzANJzNxAI7nwJ20ZSk8mzO41P4LcBiOXX5ZEwegmfo2M09JW7bG1lxrmg/ASYRo596MTZNsxXd8PnmF8JxH9jM8/0vLFyC7qxwljaRZwTm27c3etm5ER1fdOzJPi1IFFiJCmqGfMrhvfcTAQKCnsADQGWmmHmdm7SJygKbahsICiO4l4JWZq25WLlFZWlFowFtRAIotUl5k1W2q/KIpHxVFGXYJiLpxnbxdShdOEqJ0ZaZB1C399GFUiN+WH16q+w/WuLNCAAAAAElFTkSuQmCC':
            titile = detaill_info.ele('x://p[@class="title"]')
            print('>', titile.text, '   未完成')

            # 进行完成操作
            titile.click()
            page.wait.load_start(timeout=1)
            run()


        else:
            titile = detaill_info.ele('x:.//p[@class="title"]').text
            print('>', titile, '   已完成')


# 获取小章节
def get_x_chapter(chapters):
    x_chapters = chapters.eles('x:.//div[@class="first-level-inner-box"]/div')
    for x_chapter in x_chapters:
        x_chapter_title = x_chapter.ele('x:.//div[@class="p"]//span[@class="title-big"]')
        # 如果不存在标题 and 只获取课件开头的
        if not x_chapter_title:
            continue
        print('--------->', x_chapter_title.text)
        get_detail_info(x_chapter)


# 获取大章节信息
def get_chapter():
    chapters = page.eles('x:.//div[@class="left-box"]/div[@class="menu-box"]/div')[1:-1]
    for chapter in chapters:
        chapter_title = chapter.ele('x:.//p[@class="title-big"]').text
        print('\n====================', chapter_title, '====================')

        # 判断是否展开详情
        is_open = chapter.ele('x:.//div[@class="first-level-inner-box"]/@style', timeout=0.2)
        if not is_open or is_open == 'height: 0px;':
            # 展开详情
            chapter.ele('x:.//p[@class="title-big"]').click()
            time.sleep(0.2)

        get_x_chapter(chapter)


def is_logn():
    page.get('https://www.cqooc.com/index/home')
    page.wait.load_start(timeout=30)

    while True:
        page.get('https://www.cqooc.com/index/home')
        page.wait.load_start(timeout=1)

        # 查找登录按钮
        no_logn_status = page('xpath=//span[@class="login-logo"]', timeout=1)
        # 未登录
        if no_logn_status:
            print('账号未登录，请先完成登录！')
            # 执行登录操作
            username = input('请输入账号：')
            password = input('请输入密码：')
            # 登录操作
            page('xpath=//span[@class="login-logo"]', timeout=1).click()
            time.sleep(0.5)
            page.ele('xpath=//div[@class="username-box"]//input').input(username)
            page.ele('xpath=//div[@class="password-box"]//input').input(password)
            time.sleep(0.5)
            page.ele('xpath=//div[@class="submit-btn"]').click()
            time.sleep(1)

        else:
            print('账号已登录--->开始运行')
            break


def run_set():
    print(
        '项目说明：本软件只适用于智慧教育平台中《纪录片创作》课程\n\n使用方法：\n\n1.下载Chrome浏览器(如果有就不需要再下载了)\n\n>下载地址：https://www.google.cn/intl/zh-CN/chrome/\n\n2.在Chrome浏览器上登录智慧教育(刷课平台)\n\n>智慧教育：https://www.cqooc.com/index/home\n\n3.完成了以上操作后按任意键运行')
    chrom_path = input()


if __name__ == '__main__':
    run_set()
    # 页面设置
    co = ChromiumOptions()
    # 设置启动时最大化
    co.set_argument('--start-maximized')
    # 设置浏览器路径
    # co.set_browser_path(path="C:\Program Files\Google\Chrome\Application\chrome.exe")
    # 设置超时时间
    co.set_timeouts(base=0.2)
    page = ChromiumPage(co)

    # 宇宙免责声明
    print('''
    # 免责声明

    本软件及其相关文档（以下简称“软件”）仅供教育和学习目的使用。作者提供此软件时，不提供任何形式的明示或暗示的担保，包括但不限于对适销性、特定用途适用性、所有权和非侵权性的任何保证。

    在任何情况下，作者均不对任何个人或实体因使用或无法使用本软件而可能遭受的任何直接、间接、偶然、特殊、惩罚性或后果性损失承担责任，无论这些损失是基于合同、侵权行为（包括疏忽）或其他原因造成的，即使作者已被告知此类损失的可能性。

    在使用本软件时，用户应自行承担风险。作者不对任何因使用或依赖本软件而产生的损失或损害承担责任。

    用户应确保遵守所有适用的法律和法规，并对其使用本软件的行为负责。本软件不得用于任何非法目的，或者以任何非法方式使用。

    ## 有任何问题联系：2841952537
    ## 开源地址：https://github.com/2841952537/cqooc_class

    ''')
    print('等待页面加载中...预计30秒...')

    # 登录判断
    is_logn()

    # 访问页面
    page.get('https://www.cqooc.com/course/detail/courseStudy?id=dc58e3be5d477b79&kkzt=true')
    # page.get('https://www.cqooc.com/course/detail/courseStudy?id=334572312')
    page.wait.load_start(timeout=3)

    # 获取大章节信息
    get_chapter()
