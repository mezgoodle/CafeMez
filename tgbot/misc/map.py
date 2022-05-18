url = 'https://google.com/maps?q={lat},{lon}'


def show(lat, lon):
    return url.format(lat=lat, lon=lon)
