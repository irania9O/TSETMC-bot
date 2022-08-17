from html2image import Html2Image
from source.TsetmcApi import Tsetmc
from math import log10, floor
from datetime import datetime
from source import jalali

def e2p(input_str):
    numbers = {
        "0": "۰",
        "1": "١",
        "2": "۲",
        "3": "۳",
        "4": "۴",
        "5": "۵",
        "6": "۶",
        "7": "۷",
        "8": "۸",
        "9": "۹",
    }
    for english_number, persian_number in numbers.items():
        input_str = input_str.replace(english_number, persian_number)
    
    return input_str

def jalali_converter():
    jmonths = ["فروردين", "ارديبهشت", "خرداد", "تير", "مرداد", "شهريور", "مهر", "آبان", "آذر", "دي", "بهمن", "اسفند"]
    time = datetime.now()
    time_to_str = "{},{},{}".format(time.year, time.month, time.day) 
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    month_persian = jmonths[time_to_tuple[1]-1]

    output = "{} {} {}, ساعت {}:{}".format(
        time_to_tuple[2],
        month_persian,
        time_to_tuple[0],
        time.hour,
        time.minute
    )

    return e2p(output)

def humanize_number(value, significant_digits=3, strip_trailing_zeros=True):
    """
    Adaption of humanize_numbers_fp that will try to print a given number of significant digits, but sometimes more or
    less for easier reading.

    Examples:
    humanize_number(6666666, 2) = 6.7M
    humanize_number(6000000, 2) = 6M
    humanize_number(6000000, 2, strip_trailing_zeros=False) = 6.0M
    humanize_number(.666666, 2) = 0.67
    humanize_number(.0006666, 2) = 670µ
    """
    powers = [10 ** x for x in (12, 9, 6, 3, 0, -3, -6, -9)]
    human_powers = ['T', 'B', 'M', 'K', '', 'm', u'µ', 'n']
    is_negative = False
    suffix = ''

    if not isinstance(value, float):
        value = float(value)
    if value < 0:
        is_negative = True
        value = abs(value)
    if value == 0:
        decimal_places = max(0, significant_digits - 1)
    elif .001 <= value < 1:  # don't humanize these, because 3.0m can be interpreted as 3 million
        decimal_places = max(0, significant_digits - int(floor(log10(value))) - 1)
    else:
        p = next((x for x in powers if value >= x), 10 ** -9)
        i = powers.index(p)
        value = value / p
        before = int(log10(value)) + 1
        decimal_places = max(0, significant_digits - before)
        suffix = human_powers[i]

    return_value = ("%." + str(decimal_places) + "f") % value
    if is_negative:
        return_value = "-" + return_value
    if strip_trailing_zeros and '.' in return_value:
        return_value = return_value.rstrip('0').rstrip('.')

    return e2p(return_value + suffix)

class IMAGE:
    def __init__(self, code) -> None:
        self.code = code

    def create(self):
        try:
            TSE_OBJ = Tsetmc()
            code = str(self.code)
            with open('source/main.html', 'r', encoding="utf8") as file :
                filedata = file.read()

            stock_info = TSE_OBJ.company_information(code)['instrumentIdentity']
            filedata = filedata.replace("%name%", stock_info['lVal18AFC'])
            filedata = filedata.replace("%detail%", stock_info['lVal30'])


            infoTs = TSE_OBJ.get_closing_price_info(code)['closingPriceInfo']
            filedata = filedata.replace("%qTotTran5J%",humanize_number(infoTs['qTotTran5J']))
            filedata = filedata.replace("%qTotCap%",humanize_number(infoTs['qTotCap']))

            for key, value in infoTs.items():
                filedata = filedata.replace(f"%{key}%", e2p(str(value)))

            filedata = filedata.replace("%detail%", stock_info['lVal30'])

            pClosing_percentage = round((1-infoTs['priceYesterday']/infoTs['pClosing'])*100,2)
            filedata = filedata.replace("%pClosing_percentage%", e2p(str(pClosing_percentage)))
            filedata = filedata.replace("closing_pointer", str(((infoTs['pClosing']-infoTs['priceMin'])/(infoTs['priceMax']-infoTs['priceMin'])*100))+"%")
            if pClosing_percentage > 0:
                filedata = filedata.replace("pClosing_percentage_color", "#1bbf89")
            elif pClosing_percentage < 0:
                filedata = filedata.replace("pClosing_percentage_color", "#db524b")
            else:
                filedata = filedata.replace("pClosing_percentage_color", "#grey")
                
            pDrCotVal_percentage = round((1-infoTs['priceYesterday']/infoTs['pDrCotVal'])*100,2)
            filedata = filedata.replace("%pDrCotVal_percentage%", e2p(str(pDrCotVal_percentage)))
            filedata = filedata.replace("pDrCotVal_pointer", str(((infoTs['pDrCotVal']-infoTs['priceMin'])/(infoTs['priceMax']-infoTs['priceMin'])*100))+"%")

            if pClosing_percentage > 0:
                filedata = filedata.replace("pDrCotVal_percentage_color", "#1bbf89")
            elif pClosing_percentage < 0:
                filedata = filedata.replace("pDrCotVal_percentage_color", "#db524b")
            else:
                filedata = filedata.replace("pDrCotVal_percentage_color", "#grey")
                
            up_period = int(infoTs['priceYesterday']*1.05)
            down_period = int(infoTs['priceYesterday']*0.95)

            if infoTs['priceMax'] > infoTs['priceYesterday']:
                if (1-infoTs['priceMax']/up_period) == 0:
                    filedata = filedata.replace("postive_percentage", str("50%"))
                else:
                    filedata = filedata.replace("postive_percentage", str((1-infoTs['priceMax']/up_period)*500)+"%")
            else:
                filedata = filedata.replace("postive_percentage", "0%")

            if infoTs['priceMin'] < infoTs['priceYesterday']:
                if (infoTs['priceMin']/down_period-1) == 0:
                    filedata = filedata.replace("negative_percentage", str("50%"))
                else:
                    filedata = filedata.replace("negative_percentage", str((infoTs['priceMin']/down_period-1)*500)+"%")
            else:
                filedata = filedata.replace("negative_percentage", "0%")

            filedata = filedata.replace("%priceMaxperiod%", e2p(str(up_period)))
            filedata = filedata.replace("%priceMinperiod%", e2p(str(down_period)))

            base_order = """<tr>
                        <td class="count" style=";">%zOrdMeOf%</td>
                        <td style="width:40%">
                            <div class="table--price-vol">
                                <div class="table--vol-bar sell" style="width:|percentMeOf|%;"> </div>
                                <div class="flex-between">
                                    <span class="volume" style=";">%qTitMeOf%</span>
                                    <span class="price sell" style=";">%pMeOf%</span>
                                </div>
                            </div>
                        </td>
                        <td style="width:40%">
                            <div class="table--price-vol">
                                <div class="table--vol-bar buy" style="width:|percentMeDem|%"> </div>
                                <div class="flex-between">
                                    <span class="price buy" style=";">%pMeDem%</span>
                                    <span class="volume" style=";">%qTitMeDem%</span>
                                </div>
                            </div>
                        <td class="count" style=";">%zOrdMeDem%</td>
                    </tr>"""

            data = ""
            info_tse = TSE_OBJ.orders(code)['bestLimits']
            cole = 0
            for i in info_tse:
                cole += i['zOrdMeDem']
                cole += i['zOrdMeOf']

            for i in info_tse:
                tmp = base_order
                for key,value in i.items():
                    tmp = tmp.replace(f"%{key}%", e2p(str(value)))
                    if key == 'zOrdMeDem':
                        tmp = tmp.replace("|percentMeDem|", str(int(value/cole*100)))
                    elif key == 'zOrdMeOf':
                        tmp = tmp.replace("|percentMeOf|", str(int(value/cole*100)))

                data += tmp

            filedata = filedata.replace("%today%", str(data))


            info_grabbed = TSE_OBJ.buy_sell_persons_history(code)['clientType']
            buy = 0
            sell = 0

            buy += int(info_grabbed['buy_I_Volume'])
            buy += int(info_grabbed['buy_N_Volume'])
            sell += int(info_grabbed['sell_I_Volume'])
            sell += int(info_grabbed['sell_N_Volume'])

            for key,value in info_grabbed.items():
                filedata = filedata.replace(f"%{key}%", humanize_number(value))

            filedata = filedata.replace("|buy_I_Percent|", e2p(str(round(info_grabbed['buy_I_Volume']/buy,2)*100)))
            filedata = filedata.replace("|sell_I_Percent|", e2p(str(round(info_grabbed['sell_I_Volume']/buy,2)*100)))
            filedata = filedata.replace("|buy_N_Percent|", e2p(str(round(info_grabbed['buy_N_Volume']/buy,2)*100)))
            filedata = filedata.replace("|sell_N_Percent|", e2p(str(round(info_grabbed['sell_N_Volume']/buy,2)*100)))

            CHART_DATA = []
            for date, data in enumerate(TSE_OBJ.get_daily_history(code,200)["closingPriceDaily"]):
                CHART_DATA.append({"t":date,"c":int(data['pClosing']),"h":int(data['priceMax']),"l":int(data['priceMin']),"o":int(data['priceFirst']),"v":0})

            filedata = filedata.replace("CHART_DATA", str(CHART_DATA))
            filedata = filedata.replace("DATE_TIME", jalali_converter())


            with open(f'html/{code}.html', 'w', encoding="utf8") as file:
                file.write(filedata)

            hti = Html2Image(output_path="images")
            hti.screenshot(html_file=f'html/{code}.html', save_as=f'{code}.png',size=(550, 780))
            return True

        except:
            return False