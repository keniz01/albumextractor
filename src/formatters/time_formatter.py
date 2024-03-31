def duration_formatter(total_length: float) -> str:
    
    minutes, seconds = divmod(total_length, 60)
    hours, minutes = divmod(minutes, 60)

    seconds = round(seconds)
    minutes = round(minutes)
    hours = round(hours)        
    
    if hours == 0:
        return "%02d:%02d" % (minutes, seconds)
    
    return "%02d:%02d:%02d" % (hours, minutes, seconds)