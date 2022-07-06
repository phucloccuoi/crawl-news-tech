from gettext import find
from requests_html import HTMLSession, HTML
from pyppeteer import errors
from time import sleep

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

def main():
    result_page = get_session(f"https://quantrimang.com/windows-10-os", 4)

    find_link = result_page.find("a.thumb")

    for index in range(len(find_link)):
        print(index, find_link[index])

if __name__ == "__main__":
    main()
