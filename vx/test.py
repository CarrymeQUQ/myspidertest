import pdfkit
 
url='https://www.cnblogs.com/sriba/p/8043294.html'#一篇博客的url
#这里指定一下wkhtmltopdf的路径，这就是我为啥在前面让记住这个路径
pdfkit.from_url(url, 'jmeter_下载文件.pdf')