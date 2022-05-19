url = 'https://google.com/maps?q={lat},{lon}'


def show(lat, lot):
    return url.format(lat=lat, lon=lot)
