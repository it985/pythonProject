import hashlib
import re
import time

import markdown
import requests

import aurora.category
import aurora.tags
import aurora.attachment
import aurora.post

# 设置你的GitHub访问令牌
GITHUB_ACCESS_TOKEN = '123'

# 添加访问令牌到HTTP头部
headers = {
    'Authorization': f'token {GITHUB_ACCESS_TOKEN}'
}
timeout=30

# 处理评论
def handle_comment(username, repo_name, id):
    result = ''
    # 构建评论API URL
    comment_page = 1
    while True:
        url = f'https://api.github.com/repos/{username}/{repo_name}/issues/{id}/comments?page={comment_page}&per_page=100'
        response = None
        # 发送GET请求
        for i in range(3):
            try:
                response = requests.get(url, headers=headers, timeout=timeout)
                break
            except Exception as e:
                print(f"== 请求失败：{url}， 异常：{e}")
        # 检查请求是否成功
        if response.status_code != 200:
            raise Exception("查询issue评论失败：" + url)
        comments = response.json()
        if (len(comments) == 0):
            break
        for comment in comments:
            comment_name = comment['user']['login']
            body = comment['body']
            result += f'\n\n**Comment From: {comment_name}**\n\n{body}'
        comment_page = comment_page + 1
    return result

# 处理文章中的图片
def handle_image(id, title, content):
    def handle_content(match):
        text = match.group(0)
        urls = re.findall(r"src=['\"]{1}(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)", text)
        if (len(urls) == 0):
            return ''
        url = urls[0]
        new_url = aurora.attachment.upload_image("github", url)
        if new_url == None:
            print("== 上传图片失败：" + url)
            return ''
        print("== Uploaded image：" + url)
        print("== Uploaded image：" + new_url)
        print("== Uploaded image：" + text.replace(url, new_url))
        return text.replace(url, new_url)

    content = re.sub(r'<img\s+[^>]*>', handle_content, content)
    content = content.replace('alt="image"', f'alt="{title}"')
    return content

# 处理issue
def handle_issue(username, repo_name, title_prefix, since):
    # 获取文章所属的分类
    categories = aurora.category.get_category()
    categoryIds = []
    if username not in categories:
        categories[username] = aurora.category.create_category(0, username)
        print(f"创建分类：{username}")
    categoryIds.append(categories[username])
    if repo_name not in categories:
        categories[repo_name] = aurora.category.create_category(categories[username], repo_name)
        print(f"创建分类：{repo_name}")
    categoryIds.append(categories[repo_name])
    # 获取所有标签
    tags = aurora.tags.get_tags()

    # 构建评论API URL
    issue_page = 1
    while True:
        # 构建API URL
        url = f'https://api.github.com/repos/{username}/{repo_name}/issues?state=all&since={since}&page={issue_page}&per_page=100'
        # 发送GET请求
        response = None
        # 发送GET请求
        for i in range(3):
            try:
                response = requests.get(url, headers=headers, timeout=timeout)
                break
            except Exception as e:
                print(f"== 请求失败：{url}， 异常：{e}")
        # 检查请求是否成功
        if response.status_code != 200:
            raise Exception("查询issue失败：" + url)
        # 处理结果
        issues = response.json()
        if (len(issues) == 0):
            break
        for issue in issues:
            # 标题
            title = title_prefix + issue['title'].replace('`', '')
            # 标签列表
            tagIds = []
            for label in issue['labels']:
                name = label['name']
                if name not in tags:
                    tags[name] = aurora.tags.create_tag(name)
                    print(f"== 创建标签：{name}")
                tagIds.append(tags[name])
            alias = "GI" + str(issue['id'])
            # 文案内容处理
            body = '' if issue['body'] is None else issue['body']
            comment_body = handle_comment(username, repo_name, issue['number'])
            content = body + comment_body
            content = markdown.markdown(content, extensions=['markdown.extensions.extra'])
            content = handle_image(issue['id'], title, content)
            aurora.post.create_or_update_post(title, alias, content, categoryIds, tagIds)
            time.sleep(1)
        issue_page = issue_page + 1
        # break


if __name__ == '__main__':
    handle_issue('nineya', 'halo-theme-dream2.0', 'dream2.0 ', '2000-01-01T00:00:00Z')