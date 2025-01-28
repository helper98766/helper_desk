def get_proxy(self, PROXY_USERNAME, PROXY_PASSWORD):
    return {
        "http": f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@127.0.0.1:8080",
        "https": f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@127.0.0.1:8080",
    }