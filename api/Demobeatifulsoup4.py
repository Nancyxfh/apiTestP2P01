from bs4 import BeautifulSoup

h = """
<html> 
    <head>
        <title>黑马程序员</title>
    </head> 
    <body>
        <p id="test01">软件测试</p>
        <p id="test02">2020年</p>
        <a href="/api.html">接口测试</a>
        <a href="/web.html">Web自动化测试</a> 
        <a href="/app.html">APP自动化测试</a>
    </body>
</html>
"""
bs1 = BeautifulSoup(h,"html.parser")

# 1.获取整个title标签
print(bs1.title)

# 2.获取标签名
print(bs1.title.name)

# 3.获取文字
print(bs1.title.string)

# 4.获取属性
print(bs1.p.get("id"))
print(bs1.p["id"])

# 5.批量找元素
for a in bs1.find_all("a"):
    print(a.get("href"),a.string)