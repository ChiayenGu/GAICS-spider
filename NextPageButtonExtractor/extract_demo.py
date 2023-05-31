from NextPageButtonExtractor import button_extractor
import feapder


class AirSpiderDemo(feapder.AirSpider):
    def start_requests(self):
        url = "https://bjbicycle.cn/xhzl/xiehuidongtai/index_2.html"
        yield feapder.Request(url, method="GET")

    def download_midware(self, request):
        request.headers = {
            "authority": "bjbicycle.cn",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh-HK;q=0.9,zh;q=0.8",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": "https://bjbicycle.cn/xhzl/xiehuidongtai/",
            "sec-ch-ua": "\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        }
        return request

    def parse(self, request, response):
        # print(response.text)
        print(response)
        res = button_extractor(response)
        print(res)


if __name__ == "__main__":
    AirSpiderDemo(thread_count=1).start()