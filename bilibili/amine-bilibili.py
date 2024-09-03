import requests


def get_anime_info(year, page=1, pagesize=20):
    url = f'https://api.bilibili.com/pgc/season/index/result?st=1&order=3&season_version=-1&spoken_language_type=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year={year}&style_id=-1&sort=0&page={page}&season_type=1&pagesize={pagesize}&type=1'
    response = requests.get(url)

    # Print the raw response text for debugging
    print(f"Response status code: {response.status_code}")
    print("Response text:")
    print(response.text)

    # Try parsing JSON
    try:
        return response.json()
    except ValueError as e:
        print(f"Error decoding JSON: {e}")
        return None


year = 2017
data = get_anime_info(year)
print(data)
