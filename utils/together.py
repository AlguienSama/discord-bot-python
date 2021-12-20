import os
from utils.errors import CustomError
from dotenv import load_dotenv
import urllib3
import json

# fetch

defaultApplications = {
    'youtube': '755600276941176913',
    'poker': '755827207812677713',
    'betrayal': '773336526917861400',
    'fishing': '814288819477020702',
    'chess': '832012586023256104'
}

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class DiscordTogether:
    def __init__(self, applications=defaultApplications):
        self.applications = {**defaultApplications, **applications}

    async def create_together_code(self, voice_channel_id: int, option: str):

        if option is not None and self.applications[option.lower()] is not None:
            application_ID = self.applications[option.lower()]

            try:
                http = urllib3.PoolManager()

                fields = json.dumps({
                    'max_age': 86400,
                    'max_uses': 0,
                    'target_application_id': application_ID,
                    'target_type': 2,
                    'temporary': False,
                    'validate': None
                }, separators=(',', ':')).encode('utf-8')

                r = http.request(
                    'POST',
                    f'https://discord.com/api/v8/channels/{voice_channel_id}/invites',
                    body=fields,
                    headers={
                        'Authorization': f'Bot {TOKEN}',
                        'Content-Type': 'application/json'
                    }
                )

                r = json.loads(r.data.decode('utf-8'))

                if 'error' in r or 'code' not in r:
                    raise

                code = r['code']

            except Exception as e:
                raise Voice('Error !!')

            return f'https://discord.com/invite/{code}'
        else:
            raise CustomError('Invalid Option')
