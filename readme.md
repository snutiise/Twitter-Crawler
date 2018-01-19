##트위터 이미지 크롤러입니다.

사용하기 위해서는 selenium과 scrapy를 설치해야합니다.

{% highlight bash %}
$ git clone https://github.com/snutiise/Twitter-Crawler.git

$ sudo pip install selenium

$ sudo pip instal scrapy

$ cd Twitter-Crawler

$ scrapy crawl twitter
{% endhighlight %}

config 파일에서 수집하고 싶은 이미지에 대한 키워드와 페이지 수, 그리고 크롤러가 위치한 절대경로를 설정해주면 됩니다.

ex)
keyword=러블리즈
page=10
rootPath=/home/jsh/git/Twitter-Crawler/