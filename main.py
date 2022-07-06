from gettext import find
from requests_html import HTMLSession, HTML
from pyppeteer import errors
from time import sleep

new_session = HTMLSession()
time_out = 3

try:
    my_response = new_session.get('https://quantrimang.com/windows-10-os')

    try:
        my_response.html.render(scrolldown=1, sleep=time_out, keep_page=True)
    except ConnectionRefusedError:
        my_response.html.render(scrolldown=1, sleep=time_out + 1, keep_page=True)
    except RuntimeError:
        my_response.html.render(scrolldown=1, sleep=time_out + 2, keep_page=True)
    except errors.NetworkError:
        my_response.html.render(scrolldown=1, sleep=time_out - 1, keep_page=True)
    finally:
            new_session.close()
except errors.TimeoutError:
    sleep(time_out/2)
    my_response.html.render(scrolldown=1, sleep=time_out, keep_page=True)
finally:
    new_session.close()

result_page = HTML(html = my_response.html.html)

find_link = result_page.find("a.thumb")

for index in range(len(find_link)):
    print(index, find_link[index])