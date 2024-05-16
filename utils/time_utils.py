def get_milis(days = 0, hours = 0, minutes = 0):
    minutes = minutes + 60*hours + 24*60*days
    return minutes * 60 * 1000