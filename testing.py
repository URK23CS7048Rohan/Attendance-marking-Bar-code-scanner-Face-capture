import datetime 

current_time=datetime.datetime.now()
print(current_time)
hours=current_time.hour
minute=current_time.minute
converted=hours*60+minute
print(converted)
print(converted-664)