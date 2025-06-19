import base64
import json
import os
import re  # 内置模块
import subprocess

import requests  # 发送请求 第三方

headers = {
    'cookie': 'MONITOR_WEB_ID=c27b9f4a-4917-4256-be93-e948308467e3; ttcid=0cbb8baca16443e8b2320dfcb0ebd3ab24; __gads=ID=b750d35ceb3b300e-22f59bfba5d0002a:T=1645008733:RT=1645008733:S=ALNI_MZSPYii3eywVYfjuGdExhE-Dw3tLw; BD_REF=1; support_webp=true; support_avif=true; _tea_utm_cache_1300=undefined; s_v_web_id=verify_l2kdgr6l_ZlYcneu1_fb24_4lQM_A1cp_pBZKlKxvJKzJ; passport_csrf_token=7e1f1777c680a1dd9f163d6916212e62; passport_csrf_token_default=7e1f1777c680a1dd9f163d6916212e62; sid_guard=880626da6250e5535bcc3b35a5804a5c%7C1651232961%7C3023999%7CFri%2C+03-Jun-2022+11%3A49%3A20+GMT; uid_tt=d87f79c88dc25ca91c644549863616c8; uid_tt_ss=d87f79c88dc25ca91c644549863616c8; sid_tt=880626da6250e5535bcc3b35a5804a5c; sessionid=880626da6250e5535bcc3b35a5804a5c; sessionid_ss=880626da6250e5535bcc3b35a5804a5c; sid_ucp_v1=1.0.0-KGE4ZTdhODI0MjQ3Y2IyY2Y2ZmQwYjkzYTFhNDljYjdjYjdhM2U3OTgKFAjo5IrYFxDBoa-TBhgYIAw4CEAFGgJsZiIgODgwNjI2ZGE2MjUwZTU1MzViY2MzYjM1YTU4MDRhNWM; ssid_ucp_v1=1.0.0-KGE4ZTdhODI0MjQ3Y2IyY2Y2ZmQwYjkzYTFhNDljYjdjYjdhM2U3OTgKFAjo5IrYFxDBoa-TBhgYIAw4CEAFGgJsZiIgODgwNjI2ZGE2MjUwZTU1MzViY2MzYjM1YTU4MDRhNWM; odin_tt=ab7eaf992f0e5cc3871fd8fde7797f8253548498d52cd8f6320c1d408d8fb5f853f6b88fe9d3e249e91b0baac908955a; tt_scid=yZBs23biytSrdLbhg4PwtQsnp5iRak5-8X3Y.rM36zEzqMDW4OWKwf0CAfb4Sa8r725a; ttwid=1%7Cbki1kBY9AbTODWRF62oQmAFNNd1E9JpOrWrMnRcIdwY%7C1651234433%7C69cbf75423181a837f3739e9b73665b4dc82f1070d93934d5843d3ece167b776; __ac_nonce=0626bd85f00123bbca353; __ac_signature=_02B4Z6wo00f010qt8RAAAIDCKacxeDkkRtdKifWAALDLGZ5UTxtgNht0fiirvQ84GFg6fgEpzmKoOpzBna11K-91eblu7vLsme2e9DrawirS.iQkhzxxQA-2FbYMTkKz.zBC6phs4yeOUKGUc6; ixigua-a-s=3; msToken=wDc7U1VNr5xcJOObHh92pRLYNHcJkoa27rC9g9KpqtmyPZRHrp8KwNXRK82rkr2w-XEzqsGab7i_YSSrqQLCbvxl9etcaF4ElWGCvfE9-94Wyw4v8Fuq-LcizatEUIE=',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'
}
url = 'https://www.ixigua.com/7090467065097617931'
response = requests.get(url, headers=headers)
# 乱码
response.encoding = 'utf-8'
# <Response [200]>: 访问成功
html_data = response.text
# _SSR_HYDRATED_DATA=(.*?)</script>
# (.*?): 匹配任何字符 换行符除外
json_str = re.findall('_SSR_HYDRATED_DATA=(.*?)</script>', html_data)[0]
# undefined 替换为 null
json_str = json_str.replace('undefined', 'null')
json_dict = json.loads(json_str)
title = json_dict['anyVideo']['gidInformation']['packerData']['video']['title']
title = title.replace(' ', '')
video_url = json_dict['anyVideo']['gidInformation']['packerData']['video']['videoResource']['dash']['dynamic_video']['dynamic_video_list'][-1]['main_url']
audio_url = json_dict['anyVideo']['gidInformation']['packerData']['video']['videoResource']['dash']['dynamic_video']['dynamic_audio_list'][-1]['main_url']
video_url = base64.b64decode(video_url)
audio_url = base64.b64decode(audio_url)
video_url = video_url.decode()
audio_url = audio_url.decode()
# video_data = requests.get(video_url).content
with open(f'{title}.mp4', mode='wb') as f:
    f.write(video_data)
audio_data = requests.get(audio_url).content
with open(f'{title}.mp3', mode='wb') as f:
    f.write(audio_data)
ffmpeg = r'ffmpeg -i ' + title + '.mp4 -i ' + title + '.mp3 -acodec copy -vcodec copy ' + title + '-out.mp4'
subprocess.run(ffmpeg)
os.remove(f'{title}.mp3')
os.remove(f'{title}.mp4')
