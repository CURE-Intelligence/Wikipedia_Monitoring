from dotenv import load_dotenv
import os

def load_env(local_exec: bool):

    credentials = []

    if local_exec:
        env_path = "V:\\CURE\\Operations\\Clients\\DZ Privatbank\\Wikipedia Monitoring\\Page Checks\\.env"
    else:
        env_path = "//curevm/operations/Clients/DZ Privatbank/Wikipedia Monitoring/Page Checks/.env"

    load_dotenv(env_path)
    
    PATH = os.getenv('LOCAL_PATH') if local_exec else os.getenv('SERVER_PATH')
    
    return PATH