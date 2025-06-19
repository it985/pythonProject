import re
import urllib

from selenium import webdriver


def ImgSave(url,n):
    u=urllib.request.urlopen(url)
    data=u.read()
    file=open("F://pic//"+str(n)+".jpg","wb")
    file.write(data)
    file.close()

n=0
driver = webdriver.Chrome()
driver.get("https://bcy.net/login")
elem_name=driver.find_element_by_id('email')
elem_pwd=driver.find_element_by_id('password')
elem_name.send_keys("442110511@qq.com")
elem_pwd.send_keys("fuzhe631123")
driver.find_element_by_xpath('//input[@class="btn_green_w121"]').click()
driver.find_element_by_xpath("//a[@href='/illust']").click()
q=20171021
driver.find_element_by_xpath("//a[@href='/illust/toppost100']").click()
print("正在打印"+q+"的排行榜")
while(q>20171016):
    s=driver.page_source
    pattern=re.compile('work-thumbnail__topBd.*?<a href="(.*?)" target',re.S)
    imgs=re.findall(pattern,s)

    for i in imgs:
        url='https://bcy.net'+i
        driver.get(url)
        s=driver.page_source
        p = re.compile('<img class="detail_std detail_clickable" src="(.*?)"', re.S)
        ms = re.findall(p, s)

        for m in ms:
            n=n+1
            ImgSave(m,n)
    q = q - 1
    driver.get("https://bcy.net/illust/toppost100?type=week&date="+str(q))


driver.close()