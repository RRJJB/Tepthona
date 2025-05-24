
from datetime import datetime
from pytz import timezone

def get_temp_name():
    tz = timezone("Asia/Amman")
    current_time = datetime.now(tz).strftime("%I:%M:%S %p")
    return f"الاسم المؤقت: {current_time}"



def beautify_numbers(text):
    number_map = {
        '0': '𝟘', '1': '𝟙', '2': '𝟚', '3': '𝟛', '4': '𝟜',
        '5': '𝟝', '6': '𝟞', '7': '𝟟', '8': '𝟠', '9': '𝟡'
    }
    return ''.join(number_map.get(c, c) for c in text)
