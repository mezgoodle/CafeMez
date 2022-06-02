def show(lat, lot):
    url = 'https://google.com/maps?q={lat},{lon}'
    return url.format(lat=lat, lon=lot)
