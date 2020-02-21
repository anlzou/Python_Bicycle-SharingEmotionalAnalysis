'''抓取指定页面中的所有链接'''
import sys
import multiprocessing
import re
import os
import urllib.request as lib


def craw_links(url, depth, keywords, processed):
    '''url:the url to craw
     depth:the current depth to craw
     keywords:the tuple of keywords to focus
     pool:process pool
    '''
    contents = []
    if url.startswith(('http://', 'https://')):
        if url not in processed:
            # mark this url as processed
            processed.append(url)
        else:
            # avoid processing the same url again
            return
        print('Crawing ' + url + '...')
        fp = lib.urlopen(url)
        # Python3 returns bytes, so need to decode.
        contents = fp.read()
        contents_decoded = contents.decode('UTF-8')
        fp.close()
        pattern = '|'.join(keywords)
        # if this page contains certain keywords, save it to a file
        flag = False
        if pattern:
            searched = re.search(pattern, contents_decoded)
        else:
            # if the keywords to filter is not given, save current page
            flag = True
        if flag or searched:
            with open('craw\\' + url.replace(':', '_').replace('/', '_'), 'wb') as fp:
                fp.write(contents)
        # find all the links in the current page
        links = re.findall('href="(.*?)"', contents_decoded)
        # craw all links in the current page
        for link in links:
            # consider the relative path
            if not link.startswith(('http://', 'https://')):
                try:
                    index = url.rindex('/')
                    link = url[0:index + 1] + link
                except:
                    pass
            if depth > 0 and link.endswith(('.htm', '.html')):
                craw_links(link, depth - 1, keywords, processed)


if __name__ == '__main__':
    processed = []
    keywords = ('datetime', 'KeyWord2')
    if not os.path.exists('craw') or not os.path.isdir('craw'):
        os.mkdir('craw')
    craw_links(r'https://docs.python.org/3/library/index.html', 1, keywords, processed)
