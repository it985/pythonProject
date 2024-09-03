import requests, time, re, json, os, subprocess, shutil
'''
B站视频类型不同，解析规则也不同。比较烦，需要一对一写代码
'''

def get_video_data(url):
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'referer': url
    }
    req = requests.get(url=url, headers=headers)
    html = req.text
    title = re.findall('<title data-vue-meta="true">(.*?)</title>',html)[0].replace("_哔哩哔哩 (゜-゜)つロ 干杯~-bilibili","")
    title = rename_use(title)
    json_data = re.findall(r'<script>window.__playinfo__=(.*?)</script>',html)[0]
    json_data = json.loads(json_data)
    audio_url = json_data["data"]["dash"]["audio"][0]["backupUrl"][0]
    video_url = json_data["data"]["dash"]["video"][0]["backupUrl"][0]
    video_data = [title, audio_url, video_url]
    return video_data


def get_page_use(url):      # 番剧专用
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'referer': url
    }
    req = requests.get(url=url, headers=headers)
    html = req.text
    media_title = re.compile('<meta name="keywords" content="(.*?)">', re.S)
    media_title = media_title.findall(html)[0]
    media_title = rename_use(media_title)
    cid_json_comp = re.compile('<script>window.__INITIAL_STATE__=(.*?);\(function.*</script>', re.S)
    cid_json = cid_json_comp.findall(html)[0]
    videos_json = json.loads(cid_json)
    eplist = videos_json['epList']
    media = []
    for i in range(len(eplist)):
        badge = eplist[i]['badge']
        cid = eplist[i]['cid']
        title = eplist[i]['titleFormat'] + ' ' + eplist[i]['longTitle']
        title = rename_use(title)
        video = {'badge': badge, 'cid': cid, 'title': title}
        media.append(video)
    return media, media_title


def get_page_use2(url):      # 视频有选集的专用
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'referer': url
    }
    req = requests.get(url=url, headers=headers)
    html = req.text
    cid_json_comp = re.compile('<script>window.__INITIAL_STATE__=(.*?);\(function.*</script>', re.S)
    cid_json = cid_json_comp.findall(html)[0]
    videos_json = json.loads(cid_json)
    bvid = videos_json["bvid"]
    videoData = videos_json["videoData"]["pages"]
    media_title = videos_json["videoData"]["title"]
    media_title = rename_use(media_title)
    media = []
    for i in range(len(videoData)):
        cid = videoData[i]['cid']
        part = videoData[i]['part']
        title = part + str(cid)
        title = rename_use(title)
        video = {'cid': cid, 'title': title}
        media.append(video)
    return media, media_title, bvid



def get_video_url(cid):     # 番剧专用
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    base_url = 'https://api.bilibili.com/pgc/player/web/playurl?cid='
    url = base_url + str(cid) + '&fnval=80'
    r = requests.get(url, headers)
    video_json = json.loads(r.text)
    video_url = video_json["result"]["dash"]["video"][0]["backupUrl"][0]
    audio_url = video_json["result"]["dash"]["audio"][0]["backupUrl"][0]
    media = {}
    media["video_url"] = video_url
    media["audio_url"] = audio_url
    return media


def get_video_url2(cid, bvid):    # 视频有选集的专用    https://api.bilibili.com/x/player/playurl?cid=234725733&fnval=80&bvid=BV1wD4y1o7AS
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    base_url = 'https://api.bilibili.com/x/player/playurl?cid='
    url = base_url + str(cid) + '&fnval=80&bvid=' + bvid
    r = requests.get(url, headers)
    video_json = json.loads(r.text)
    video_url = video_json["data"]["dash"]["video"][0]["backupUrl"][0]
    audio_url = video_json["data"]["dash"]["audio"][0]["backupUrl"][0]
    media = {}
    media["video_url"] = video_url
    media["audio_url"] = audio_url
    return media


def video_down(badge, cid, title, media_title):    # 番剧专用
    media = get_video_url(cid)
    if badge == '':
        video_url = media["video_url"]
        audio_url = media["audio_url"]
        try:
            if not os.path.exists(media_title):
                os.mkdir(media_title)
        except:
            pass
        print(f'当前正在下载:{title}.mp4 视频，请稍等片刻...')
        downloadFile(title+'.mp4', video_url)
        print(title+'.mp4',' 视频文件下载成功!')
        print(f'当前正在下载:{title}.mp3 音频...')
        downloadFile(title+'.mp3', audio_url)
        print(title+".mp3", ' 音频文件下载成功!')
        time.sleep(2)
        merge_video(title, media_title)
    else:
        print(title, '不可下载 或需开通大会员')


def video_down2(cid, title, media_title, bvid):       # 视频选集专用
    media = get_video_url2(cid, bvid)
    video_url = media["video_url"]
    audio_url = media["audio_url"]
    try:
        if not os.path.exists(media_title):
            os.mkdir(media_title)
    except:
        pass
    print(f'当前正在下载:{title}.mp4 视频，请稍等片刻...')
    downloadFile(title+'.mp4', video_url)
    print(title+'.mp4',' 视频文件下载成功!')
    print(f'当前正在下载:{title}.mp3 音频...')
    downloadFile(title+'.mp3', audio_url)
    print(title+".mp3", ' 音频文件下载成功!')
    time.sleep(2)
    merge_video(title, media_title)



def merge_video(title, media_title):
    os.rename(title + ".mp3", "1.mp3")
    os.rename(title + ".mp4", "1.mp4")
    shutil.move("1.mp4", "ffmpeg\\bin\\1.mp4")
    shutil.move("1.mp3", "ffmpeg\\bin\\1.mp3")
    print("正在合并 " + title + "的视频...")
    os.chdir("ffmpeg\\bin\\")
    subprocess.call("ffmpeg -i 1.mp4 -i 1.mp3 -c:v copy -c:a aac -strict experimental output.mp4", shell=True)
    os.remove("1.mp4")
    os.remove("1.mp3")
    os.rename("output.mp4", title+".mp4")
    shutil.move(title+".mp4", f"..\\..\\{media_title}\\{title}.mp4")
    print("完成合并 " + title + "的视频！")
    os.chdir('../../')


def downloadFile(name, url):
    header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36","referer": "https://message.bilibili.com/"}
    r = requests.get(url, stream=True, headers=header)
    length = float(r.headers['content-length'])
    f = open(name, 'wb')
    count = 0
    count_tmp = 0
    time1 = time.time()
    for chunk in r.iter_content(chunk_size=2048):
        if chunk:
            f.write(chunk)
            count += len(chunk)
            if time.time() - time1 > 2:
                p = count / length * 100
                speed = (count - count_tmp) / 1024  / 2
                count_tmp = count
                print(name + ': complete ' + formatFloat(p) + '%' + '  下载Speed: ' + formatFloat(speed) + 'KB/S')
                time1 = time.time()
    f.close()


def formatFloat(num):
    return '{:.2f}'.format(num)

def rename_use(file_name):
    file_name = file_name.replace("\\", '').replace("/", '').replace(":", '').replace("*", '').replace("?",'').replace('"', '').replace("<", '').replace(">", '').replace("|", '')
    return file_name


def video(url):
    video = get_video_data(url)
    title = video[0]
    audio_url = video[1]
    video_url = video[2]
    try:
        if not os.path.exists('视频下载'):
            os.mkdir('视频下载')
    except:
        pass
    print(f'当前正在下载:{title}.mp4 视频，请稍等片刻...')
    downloadFile(title + '.mp4', video_url)
    print(title + '.mp4', ' 视频文件下载成功!')
    print(f'当前正在下载:{title}.mp3 音频...')
    downloadFile(title + '.mp3', audio_url)
    print(title + ".mp3", ' 音频文件下载成功!')
    time.sleep(1)
    merge_video(title, "视频下载")


def 番剧(url):
    video_all = get_page_use(url)
    for video in video_all[0]:
        video_down(video["badge"], video["cid"], video["title"], video_all[1])


def 视频选集(url):
    video_all = get_page_use2(url)
    for video in video_all[0]:
        video_down2(video["cid"], video["title"], video_all[1], video_all[2])


if __name__ == '__main__':
    print("="*50 + " 欢迎使用B站视频下载器 " + "="*50)
    print(" "*40 +'(仅供学习使用,付费视频不支持下载哦~)')
    inp = input("请将视频网址粘贴到这里： \n")
    try:
        if "www.bilibili.com/bangumi/play/" in inp:
            番剧(url=inp)
            print("下载完成，视频保存在此程序所在的文件夹内")
            time.sleep(3)
        elif "www.bilibili.com/video/" in inp:
            try:
                视频选集(url=inp)
                print("下载完成，视频保存在此程序所在的文件夹内")
                time.sleep(3)
            except:
                video(url=inp)
                print("下载完成，视频保存在此程序所在的文件夹内")
                time.sleep(3)
        else:
            print("输入有误，或不支持下载")
            time.sleep(3)
    except:
        print("当前链接不支持下载，或需开通大会员")
        time.sleep(3)