import time
def safe_api_call(func, retries=3, delay=2, critical=False):
    for i in range(retries):
        try:
            return func()
        except Exception as e:
            print(f"API error: {e} | retry {i+1}/{retries}")
            time.sleep(delay)

    if critical:
        raise Exception("Critical API failure")
    return None