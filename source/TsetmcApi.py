# http://main.tsetmc.com/InstInfo/25244329144808274
from requests import get
from json import loads


class Tsetmc:
    def __init__(self) -> None:
        pass

    def api(self, path, method, *arg):
        """
        Task:
            Excuting get method.

        Arguments:
            path                       -- api path        -- type: str     -- default: does not have
            method                     -- path method     -- type: str     -- default: does not have

        Return :
            HAVE PROBLEM               -- Exception       -- type: json     -- value: dictonary
            DOEST NOT HAVE PROBLEM     -- Json Object     -- type: json     -- value: dictonary
        """
        url_base = "http://cdn.tsetmc.com/api"
        headers = {
            "host": "cdn.tsetmc.com",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36",
            "Origin": "http://main.tsetmc.com",
            "Referer": "http://main.tsetmc.com/",
        }

        url = url_base + "/" + path + "/" + method + "/" + "/".join(list(map(str, arg)))

        response = get(url, headers=headers)
        if response.status_code == 200:
            return loads(response.text)
        else:
            raise Exception(
                f"An error ocurred during request to tsetmc, error status code: {response.status_code}"
            )

    def search(self, name):
        """
        Task:
            Search stocks by stocks name.

        Api Url:
            URL                        -- http://cdn.tsetmc.com/api/Instrument/GetInstrumentSearch/{name}

        Arguments:
            name                       -- stocks name     -- type: str      -- default: does not have

        Return :
            HAVE PROBLEM               -- Exception       -- type: json     -- value: dictonary
            DOEST NOT HAVE PROBLEM     -- Json Object     -- type: json     -- value: dictonary
        """
        return self.api("Instrument", "GetInstrumentSearch", name)

    def get_closing_price_info(self, code):
        """
        Task:
            Search stocks by stocks name.

        Api Url:
            URL                        -- http://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceInfo/{code}

        Arguments:
            name                       -- stocks name     -- type: str      -- default: does not have

        Return :
            HAVE PROBLEM               -- Exception       -- type: json     -- value: dictonary
            DOEST NOT HAVE PROBLEM     -- Json Object     -- type: json     -- value: dictonary
        """
        return self.api("ClosingPrice", "GetClosingPriceInfo", code)

    def get_daily_history(self, code, count=1):
        """
        Task:
            Get daily history by stocks id.

        Api Url:
            URL                        -- http://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceDailyList/{code}/{count}

        Arguments:
            code                       -- stocks id          -- type: +int     -- default: does not have
            count                      -- number of days     -- type: +int     -- default: 1
             *tip                      -- count =  0         -- return: all days
             *tip                      -- count != 0         -- return: according to the number of days

        Return :
            HAVE PROBLEM               -- Exception          -- type: json     -- value: dictonary
            DOEST NOT HAVE PROBLEM     -- Json Object        -- type: json     -- value: dictonary
        """
        return self.api("ClosingPrice", "GetClosingPriceDailyList", code, count)

    def history(self, code):
        """
        Task:
            Get all history by stocks id.

        Api Url:
            URL                        -- http://cdn.tsetmc.com/api/ClientType/GetClientTypeHistory/{code}

        Arguments:
            code                       -- stocks id          -- type: +int     -- default: does not have

        Return :
            HAVE PROBLEM               -- Exception          -- type: json     -- value: dictonary
            DOEST NOT HAVE PROBLEM     -- Json Object        -- type: json     -- value: dictonary
        """
        return self.api("ClientType", "GetClientTypeHistory", code)

    def orders(self, code):
        """
        Task:
            Get orders by stocks id.

        Api Url:
            URL                        -- http://cdn.tsetmc.com/api/BestLimits/{code}

        Arguments:
            code                       -- stocks id          -- type: +int     -- default: does not have

        Return :
            HAVE PROBLEM               -- Exception          -- type: json     -- value: dictonary
            DOEST NOT HAVE PROBLEM     -- Json Object        -- type: json     -- value: dictonary
        """
        return self.api("BestLimits", code)

    def buy_sell_persons_history(self, code):
        """
        Task:
            Get buy sell persons history by stocks id.

        Api Url:
            URL                        -- http://cdn.tsetmc.com/api/ClientType/GetClientType/{code}/1/0

        Arguments:
            code                       -- stocks id          -- type: +int     -- default: does not have

        Return :
            HAVE PROBLEM               -- Exception          -- type: json     -- value: dictonary
            DOEST NOT HAVE PROBLEM     -- Json Object        -- type: json     -- value: dictonary
        """
        return self.api("ClientType", "GetClientType", code, "1", "0")

    def supervisor_messages(self, code):
        """
        Task:
            Get supervisor messages by stocks id.

        Api Url:
            URL                        -- http://cdn.tsetmc.com/api/Msg/GetMsgByInsCode/{code}

        Arguments:
            code                       -- stocks id          -- type: +int     -- default: does not have

        Return :
            HAVE PROBLEM               -- Exception          -- type: json     -- value: dictonary
            DOEST NOT HAVE PROBLEM     -- Json Object        -- type: json     -- value: dictonary
        """
        return self.api("Msg", "GetMsgByInsCode", code)

    def company_information_codal(self, name):
        """
        Task:
            Get company information codal by stocks name.

        Api Url:
            URL                        -- http://cdn.tsetmc.com/api/Codal/GetCodalPublisherBySymbol/{name}

        Arguments:
            name                       -- stocks name        -- type: +int     -- default: does not have

        Return :
            HAVE PROBLEM               -- Exception          -- type: json     -- value: dictonary
            DOEST NOT HAVE PROBLEM     -- Json Object        -- type: json     -- value: dictonary
        """
        return self.api("Codal", "GetCodalPublisherBySymbol", name)

    def company_information(self, code):
        """
        Task:
            Get company information by stocks stocks id.

        Api Url:
            URL                        -- http://cdn.tsetmc.com/api/Instrument/GetInstrumentIdentity/{code}

        Arguments:
            code                       -- stocks id          -- type: +int     -- default: does not have

        Return :
            HAVE PROBLEM               -- Exception          -- type: json     -- value: dictonary
            DOEST NOT HAVE PROBLEM     -- Json Object        -- type: json     -- value: dictonary
        """
        return self.api("Instrument", "GetInstrumentIdentity", code)

    def holders(self, code):
        """
        Task:
            Get holders by stocks stocks id.

        Api Url:
            URL                        -- http://cdn.tsetmc.com/api/Shareholder/GetInstrumentShareHolderLast/{code}

        Arguments:
            code                       -- stocks id          -- type: +int     -- default: does not have

        Return :
            HAVE PROBLEM               -- Exception          -- type: json     -- value: dictonary
            DOEST NOT HAVE PROBLEM     -- Json Object        -- type: json     -- value: dictonary
        """
        return self.api("Shareholder", "GetInstrumentShareHolderLast", code)

    def board_of_directors(self, code):
        """
        Task:
            Get board of directors by stocks stocks id.

        Api Url:
            URL                        -- http://cdn.tsetmc.com/api/Codal/GetStatementContentByInsCode/12/0/-1/{code}

        Arguments:
            code                       -- stocks id          -- type: +int     -- default: does not have

        Return :
            HAVE PROBLEM               -- Exception          -- type: json     -- value: dictonary
            DOEST NOT HAVE PROBLEM     -- Json Object        -- type: json     -- value: dictonary
        """
        return self.api("Codal", "GetStatementContentByInsCode", "12", "0", "-1", code)

    def balance_sheet(self, code):
        """
        Task:
            Get balance sheet by stocks stocks id.

        Api Url:
            URL                        -- http://cdn.tsetmc.com/api/Codal/GetStatementContentByInsCode/6/6/0/{code}

        Arguments:
            code                       -- stocks id          -- type: +int     -- default: does not have

        Return :
            HAVE PROBLEM               -- Exception          -- type: json     -- value: dictonary
            DOEST NOT HAVE PROBLEM     -- Json Object        -- type: json     -- value: dictonary
        """
        return self.api("Codal", "GetStatementContentByInsCode", "6", "6", "0", code)

    def assembly_decisions(self, code):
        """
        Task:
            Get assembly decisions by stocks stocks id.

        Api Url:
            URL                        -- http://cdn.tsetmc.com/api/Codal/GetStatementContentByInsCode/14/0/-1/{code}

        Arguments:
            code                       -- stocks id          -- type: +int     -- default: does not have

        Return :
            HAVE PROBLEM               -- Exception          -- type: json     -- value: dictonary
            DOEST NOT HAVE PROBLEM     -- Json Object        -- type: json     -- value: dictonary
        """
        return self.api("Codal", "GetStatementContentByInsCode", "14", "0", "-1", code)

    def statistics(self, code):
        """
        Task:
            Get statistics by stocks stocks id.

        Api Url:
            URL                        -- http://cdn.tsetmc.com/api/MarketData/GetInstrumentStatistic/{code}

        Arguments:
            code                       -- stocks id          -- type: +int     -- default: does not have

        Return :
            HAVE PROBLEM               -- Exception          -- type: json     -- value: dictonary
            DOEST NOT HAVE PROBLEM     -- Json Object        -- type: json     -- value: dictonary
        """
        return self.api("MarketData", "GetInstrumentStatistic", code)

    def notifications(self, code, count=100):
        """
        Task:
            Get statistics by stocks stocks id.

        Api Url:
            URL                        -- http://cdn.tsetmc.com/api/Codal/GetPreparedDataByInsCode/{count}/{code}

        Arguments:
            code                       -- stocks id                   -- type: +int     -- default: does not have
            count                      -- number of notifications     -- type: +int     -- default: 100

        Return :
            HAVE PROBLEM               -- Exception                   -- type: json     -- value: dictonary
            DOEST NOT HAVE PROBLEM     -- Json Object                 -- type: json     -- value: dictonary
        """
        return self.api("Codal", "GetPreparedDataByInsCode", count, code)

    def bours_info(self):
        """
        Task:
            Get bours info.

        Api Url:
            URL                        -- http://cdn.tsetmc.com/api/MarketData/GetMarketOverview/1

        Arguments:
            ---

        Return :
            HAVE PROBLEM               -- Exception          -- type: json     -- value: dictonary
            DOEST NOT HAVE PROBLEM     -- Json Object        -- type: json     -- value: dictonary
        """
        return self.api("MarketData", "GetMarketOverview", "1")

    def frabours_info(self):
        """
        Task:
            Get bours info.

        Api Url:
            URL                        -- http://cdn.tsetmc.com/api/MarketData/GetMarketOverview/2

        Arguments:
            ---

        Return :
            HAVE PROBLEM               -- Exception          -- type: json     -- value: dictonary
            DOEST NOT HAVE PROBLEM     -- Json Object        -- type: json     -- value: dictonary
        """
        return self.api("MarketData", "GetMarketOverview", "2")
