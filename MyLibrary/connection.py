from datetime import datetime
import socket
import requests

class Connection(object):
    @staticmethod
    def internetReady(host: str ="8.8.8.8", port: int = 53, timeout: int =3):
        """
        Host: 8.8.8.8 (google-public-dns-a.google.com)
        OpenPort: 53/tcp
        Service: domain (DNS/TCP)
        return: `True` if Have Internet Connection
        return: `False` if not Have Internet Connection
        """
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error as ex:
            print(ex)
            return False

    @staticmethod
    def getData(host: str):
        r"""Get Data with HTTPRequest to API.

        :param url: URL for the new :class:`Request` object.
        :return: `True` and `JSON` if get data successfull
        :return: `False` if get data failed
        :rtype: `bool`, `json`
        """

        try:
            date = datetime.now()
            print(f"{date} : getting status...")
            header = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0"}
            response = requests.get(host, headers=header)
            status_code = response.status_code
            if status_code == 404:
                print("404 Not Found")
                return False, {}
            
            json = response.json()
            return True, json
        except ConnectionError as errconn:
            print(f"Connection Error: {errconn}")
            return False, {}

    @staticmethod
    def resetData(host: str):
        # reset table status
        header = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0"}
        response = requests.post(host,headers=header)
        if response.status_code != 404:
            print(response.json())
