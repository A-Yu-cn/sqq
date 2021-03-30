class GlobalData(object):

    __instance = None
    base_url = "https://sqq.12138.site:1234"
    client = None
    proxies = {
        'http': None,
        'https': None
    }

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance


