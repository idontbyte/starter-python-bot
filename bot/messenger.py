import logging
import random

logger = logging.getLogger(__name__)

class Messenger(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients

    def send_message(self, channel_id, msg):
        # in the case of Group and Private channels, RTM channel payload is a complex dictionary
        if isinstance(channel_id, dict):
            channel_id = channel_id['id']
        logger.debug('Sending msg: {} to channel: {}'.format(msg, channel_id))
        channel = self.clients.rtm.server.channels.find(channel_id)
        channel.send_message("{}".format(msg.encode('ascii', 'ignore')))

    def write_help_message(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = '{}\n{}\n{}\n{}'.format(
            "I am pollbot - tell me what to do:",
            "> `<@" + bot_uid + "> setapi` - sets the API url for posting collected data",
            "> `<@" + bot_uid + "> getbugs` - I will message everyone in channel to see if they have any bugs to report this week")
        self.send_message(channel_id, txt)
        
    def write_prompt(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = "I'm sorry, I didn't quite understand... Can I help you? (e.g. `<@" + bot_uid + "> help`)"
        self.send_message(channel_id, txt)

    def write_error(self, channel_id, err_msg):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)

    def get_bugs(self, channel_id):
        txt = "Please can you tell me - are there any open bugs to report this week?"
        response = self.clients.web.channels.info(channel_id)
        for user in response.body['channel']['members']:
            member = self.clients.web.users.info(user)
            self.clients.web.chat.post_message("@" + member.body['user']['name'], txt, as_user='true')
            
    def set_api(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = "Please tell me the API URL with `<@" + bot_uid + "> api-http://yoururl`"
        self.send_message(channel_id, txt)
   
            
            
        
