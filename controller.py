bot_running = False

def start():
    global bot_running
    bot_running = True

def stop():
    global bot_running
    bot_running = False

def is_running():
    return bot_running