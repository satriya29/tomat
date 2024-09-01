import requests
import time
from colorama import Fore, Style, init
import json
from datetime import datetime, timedelta, timezone
import random
import urllib.parse

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en,en-US;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://mini-app.tomarket.ai',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://mini-app.tomarket.ai/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Android WebView";v="126"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': 'Android',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Linux; Android 13; M2012K11AG Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.134 Mobile Safari/537.36',
    'x-requested-with': 'org.telegram.messenger.web'
}


def get_balance(token):
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/user/balance'
    headers['Authorization'] = token
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def claim_daily(token):
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/daily/claim'
    headers['Authorization'] = token
    payload = {"game_id": "fa873d13-d831-4d6f-8aee-9cff7a1d0db1"}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json(), response.status_code
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None, None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None, None

def start_farming(token):
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/farm/start'
    headers['Authorization'] = token
    payload = {"game_id": "53b22103-c7ff-413d-bc63-20f6fb806a07"}
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json(), response.status_code
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None, None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None, None
    
def claim_farming(token):
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/farm/claim'
    headers['Authorization'] = token
    payload = {"game_id": "53b22103-c7ff-413d-bc63-20f6fb806a07"}
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json(), response.status_code
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None, None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None, None

def play_game(token):
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/game/play'
    headers['Authorization'] = token
    payload = {"game_id": "59bcd12e-04e2-404c-a172-311a0084587d"}
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json(), response.status_code
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None, None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None, None

def claim_game(token,point):
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/game/claim'
    headers['Authorization'] = token
   
    payload = {"game_id": "59bcd12e-04e2-404c-a172-311a0084587d", "points": point}
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json(), response.status_code
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Token Invalid")
        return None, None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None, None

 

def main():
    tokens = []
    try:
        with open('peler.txt', 'r') as token_file:
            tokens = [token.strip() for token in token_file.readlines()]
    except FileNotFoundError:
        print(f"{Fore.RED+Style.BRIGHT}File peler.txt not found!{Style.RESET_ALL}")
        return
    
    if not tokens:
        print(f"{Fore.RED+Style.BRIGHT}No tokens available!{Style.RESET_ALL}")
        return

    print_welcome_message()

    for i, token in enumerate(tokens):
        try:
            print(f"{Fore.YELLOW+Style.BRIGHT}Processing account {i + 1}/{len(tokens)}...", flush=True)
            
            print(f"{Fore.YELLOW+Style.BRIGHT}Checking account balance...", flush=True)
            balance_response = get_balance(token)
            if balance_response is not None:
                balance = int(float(balance_response['data'].get('available_balance', 0)))
                tiket = balance_response['data'].get('play_passes', 0)
                print(f"{Fore.GREEN+Style.BRIGHT}[ Balance ]: {balance} {Style.RESET_ALL}")
                print(f"{Fore.GREEN+Style.BRIGHT}[ Tiket ]: {tiket} {Style.RESET_ALL}")
                
                # Daily claim
                print(f"{Fore.YELLOW+Style.BRIGHT}[ Daily ]: Claiming...", flush=True)
                daily, daily_status_code = claim_daily(token)
                if daily_status_code == 400 and daily['message'] == 'already_check':
                    day = daily['data']['check_counter']
                    point = daily['data']['today_points']
                    print(f"{Fore.GREEN+Style.BRIGHT}[ Daily ]: Day {day} Already checked in | {point} Points {Style.RESET_ALL}")
                elif daily_status_code == 200:
                    day = daily['data']['check_counter']
                    point = daily['data']['today_points']
                    print(f"{Fore.GREEN+Style.BRIGHT}[ Daily ]: Day {day} Claimed | {point} Points {Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED+Style.BRIGHT}[ Daily ]: Claim failed {daily} {Style.RESET_ALL}")
                
                # Start farming
                print(f"{Fore.YELLOW+Style.BRIGHT}[ Farming ]: Starting farming...", flush=True)
                farming, farming_status_code = start_farming(token)
                if farming_status_code == 200:
                    end_time = datetime.fromtimestamp(farming['data']['end_at'])
                    remaining_time = end_time - datetime.now()
                    hours, remainder = divmod(remaining_time.total_seconds(), 3600)
                    minutes, _ = divmod(remainder, 60)
                    print(f"{Fore.GREEN+Style.BRIGHT}[ Farming ]: Started. Claim in: {int(hours)} hours {int(minutes)} minutes {Style.RESET_ALL}")
                elif farming_status_code == 500 and farming['message'] == 'game already started':
                    end_time = datetime.fromtimestamp(farming['data']['end_at'])
                    remaining_time = end_time - datetime.now()
                    hours, remainder = divmod(remaining_time.total_seconds(), 3600)
                    minutes, _ = divmod(remainder, 60)
                    print(f"{Fore.CYAN+Style.BRIGHT}[ Farming ]: Already Started. Claim in: {int(hours)} hours {int(minutes)} minutes {Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED+Style.BRIGHT}[ Farming ]: Failed to start {farming} {Style.RESET_ALL}")

                # Play game if tickets are available
                while tiket > 0:
                    print(f"{Fore.GREEN+Style.BRIGHT}[ Game ]: Starting game...", flush=True)
                    play, play_status = play_game(token)
                    if play_status == 200:
                        print(f"{Fore.GREEN+Style.BRIGHT}[ Game ]: Game started! {Style.RESET_ALL}")
                        time.sleep(30)  # Simulate game play time
                        print(f"{Fore.YELLOW+Style.BRIGHT}[ Game ]: Claiming game points...", flush=True)
                        point = random.randint(400, 600)
                        claim, claim_status = claim_game(token, point)
                        if claim_status == 200:
                            print(f"{Fore.GREEN+Style.BRIGHT}[ Game ]: Success. Earned {point} Points {Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED+Style.BRIGHT}[ Game ]: Failed to claim points! {Style.RESET_ALL}")
                        tiket -= 1
                    else:
                        print(f"{Fore.RED+Style.BRIGHT}[ Game ]: Failed to start game! {Style.RESET_ALL}")
                        break

            else:
                print(f"{Fore.RED+Style.BRIGHT}[ Balance ]: Failed to retrieve balance {Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED+Style.BRIGHT}An error occurred: {str(e)}{Style.RESET_ALL}")
            print(f"Error occurred at: {datetime.now()}")

    print(Fore.BLUE + Style.BRIGHT + f"\n==========ALL ACCOUNTS PROCESSED==========\n", flush=True)
    time.sleep(1800)  # 30 minutes delay before looping again


from datetime import datetime, timedelta, timezone
start_time = datetime.now()
def print_welcome_message():
    print(r"""
   ▄▄▄▄▀ █    ▄█  ▄▄ █    ▄   ▄█ ██▄   ▄█    ▄▄▄▄▀ ▀▄    ▄ 
▀▀▀ █    █    ██ █   █     █  ██ █  █  ██ ▀▀▀ █      █  █  
    █    █    ██  ▀▀▀█  █   █ ██ █   █ ██     █       ▀█   
   █     ███▄ ▐█     █  █   █ ▐█ █  █  ▐█    █        █    
  ▀          ▀ ▐      █ █▄ ▄█  ▐ ███▀   ▐   ▀       ▄▀     
                       ▀ ▀▀▀                           
          """)
    print(Fore.GREEN + Style.BRIGHT + "Tomarket BOT recode")
    current_time = datetime.now()
    up_time = current_time - start_time
    days, remainder = divmod(up_time.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(Fore.CYAN + Style.BRIGHT + f"Up time bot: {int(days)} hari, {int(hours)} jam, {int(minutes)} menit, {int(seconds)} detik\n\n")



if __name__ == "__main__":
    main()