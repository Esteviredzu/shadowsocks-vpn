from telethon.sync import TelegramClient
import time
import os
import CONFIG
import json, re

def extract_config(text):
    server_match = re.search(r'server:\s*([\d\.]+)', text)
    server_port_match = re.search(r'server_port:\s*(\d+)', text)
    password_match = re.search(r'password:\s*(\S+)', text)
    method_match = re.search(r'method:\s*(\S+)', text)
    
    if server_match and server_port_match and password_match and method_match:
        server = server_match.group(1)
        server_port = int(server_port_match.group(1))
        password = password_match.group(1)
        method = method_match.group(1)
        
        config = {
            "server": server,
            "server_port": server_port,
            "local_port": 1080,
            "password": password,
            "method": method
        }

        return config
    else:
        return None

def save_to_json(ss_config):
    with open('ss_config.json', 'w') as json_file:
        json.dump(ss_config, json_file, indent=4)


api_id = CONFIG.api_id
api_hash = CONFIG.api_hash

client = TelegramClient('user_session', api_id, api_hash)

async def main():
    async with client:
        await client.send_message('@vpn4peace_bot', '/legacy')
        time.sleep(4)
        messages = await client.get_messages('@vpn4peace_bot', limit=2)
        try:
            ss_config = extract_config(messages[1].message)
            save_to_json(ss_config)
            print("CONFIG UPDATED SUCCESFULLY!")
        except Exception as e:
            print(f'error: {e}')
client.loop.run_until_complete(main())

