from requests_html import HTMLSession, HTML
from pyppeteer import errors
from time import sleep
from bs4 import BeautifulSoup

# Hàm tạo một phiên kết nối vào một website với liên kêt cho trước
def get_session(url_full, time_out):
    '''
    - Chức năng: tạo một phiên kết nối vào một website với liên kêt cho trước
    - url_full: địa chỉ website muốn truy cập
    - time_out: Thời gian phản hồi của website, sau đó sẽ đóng
    - result_page: hàm trả về biến loại HTML lưu toàn bộ thông tin html của website
    '''
    # Khởi tạo một phiên kết nối
    my_session = HTMLSession()

    try:
        # Tạo một phiên kết nối tới trang đích
        my_response = my_session.get(url_full)

        # Tổng thời gian Loading bằng thời gian tối đa là 6s + 2s và tối thiểu là 2s + 2s
        try:
            my_response.html.render(scrolldown=1, sleep=time_out, keep_page=True)
        except ConnectionRefusedError:
            my_response.html.render(scrolldown=1, sleep=time_out + 1, keep_page=True)
        except RuntimeError:
            my_response.html.render(scrolldown=1, sleep=time_out + 2, keep_page=True)
        except errors.NetworkError:
            my_response.html.render(scrolldown=1, sleep=time_out - 1, keep_page=True)
        except ConnectionError:
            my_response.html.render(scrolldown=1, sleep=time_out - 2, keep_page=True)
        finally:
            my_session.close()
    except errors.TimeoutError:
        sleep(time_out/2)
        my_response.html.render(scrolldown=1, sleep=time_out, keep_page=True)
    finally:
        my_session.close()

    # Lưu kết quả trả về với định dạng theo kiểu HTML
    result_page = HTML(html = my_response.html.html)

    return result_page
# Kết thúc hàm tạo một phiên kết nối vào một website với liên kêt cho trước

# Hàm hoàn thành link bài viết
def complete_post_links(list_short_link, piece_link):
    '''
    - Chức năng: Thêm các tiền tố tên miền để hoàn thành link có thể truy cập
    - list_short_link: danh sách các link chưa được hoàn chỉnh
    - piece_link: là tiền tố cần thêm vào link
    - return: hàm trả về danh sách link có thể truy cập
    '''

    # Vòng lặp duyệt và thêm các phần còn thiếu
    for index in range(len(list_short_link)):
        list_short_link[index] = piece_link + list_short_link[index]
    
    return list_short_link
# Kết thúc hàm hoàn thành link bài viết

# Hàm truy cập vào bài viết
def access_posts(link_post):
    # Gọi hàm tạo ra phiên truy cập mới
    respone_post = get_session(link_post, 3)

    content_post = respone_post.find('div.content-detail')
    
    with open('test.txt', 'w+', encoding='utf-8') as file_test:

        file_test.write(str(content_post))
    file_test.close()
    return 1
# Kết thúc hàm truy cập vào bài viết

def main():
    # result_page = get_session(f"https://quantrimang.com/windows-10-os", 3)

    # find_link = result_page.find("a.thumb")

    # list_short_links = []

    # for index in range(len(find_link)):
    #     list_short_links.append((find_link[index]).attrs['href'])
    
    # list_full_links = complete_post_links(list_short_links, 'https://quantrimang.com/')

    # access_posts(list_full_links[0])

    respone_post = get_session('https://quantrimang.com/han-che-windows-defender-su-dung-cpu-171830', 3)

    content_post = respone_post.find('div.content-detail', first=True)

    soup = BeautifulSoup(content_post.html, 'html.parser')
    
    for tag in soup.find_all('div', class_='adbox'):
        tag.decompose()
    for tag in soup.find_all('div', class_='adszone'):
        tag.decompose()
    for tag in soup.find_all('div', class_='adslogo'):
        tag.decompose()
    
    with open('test.txt', 'w+', encoding='utf-8') as file_test:

        file_test.write(str(soup))
    file_test.close()

if __name__ == "__main__":
    main()
