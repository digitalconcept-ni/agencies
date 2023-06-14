from datetime import datetime


def elapsedtime(validate):
    data = {}
    try:
        time1 = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")  # Time now
        time2 = datetime.strptime(validate, "%Y-%m-%d %H:%M:%S.%f")  # Time validate from database
        timeElapsed = time1 - time2
        timeElapsedHours = timeElapsed.__str__().split(',')[1][:-7]
        data['days'] = timeElapsed.days
        data['hours'] = timeElapsedHours

        return data
    except Exception as e:
        data['error'] = str(e)
    return data


# validate = '2023-06-02 16:45:25.287226'
# validate = '2023-06-02'
# print(elapsedtime(validate))
