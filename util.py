import os, time

def load_configuration():
    api_key = os.getenv('API_KEY_ESPM')
    api_url = os.getenv('API_URL_ESPM')
    return api_key, api_url


def control_rate(query_limit=50):
    global last_query_time

    elapsed_time = time.time() - last_query_time
    if elapsed_time < (60 / query_limit):
        time.sleep((60 / query_limit) - elapsed_time)

    last_query_time = time.time()
    

last_query_time = 0