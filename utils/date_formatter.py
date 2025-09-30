def get_ordinal(number):
    if 10 <= number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")
    return f"{number}{suffix}"

def format_datetime(current_time):
    day_with_suffix = get_ordinal(current_time.day)
    return current_time.strftime(f"%A {day_with_suffix} %B %Y at %H:%M%p")