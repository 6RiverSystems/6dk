from uuid import uuid4

import requests


class Rule():

    def __init__(self, rules_dictionary, app_config):
        self.rules_dictionary = rules_dictionary
        self.app_config = app_config

    def get_messages_list(self, tag, exclude=['response']):
        return [
            message['message_type']
            for message in self.rules_dictionary['messages']
            if tag in message['tags']
            and set(message['tags']).isdisjoint(exclude)
        ]

    def get_message_transports(self, message_settings):
        message = next((
            rule
            for rule in self.rules_dictionary['messages']
            if rule['message_type'] == message_settings['name']),
            None)
        return message['valid_transports']

    def get_transporter_rules(self, message_type, message_transport,
                              message_format):
        message = next((rule for rule in self.rules_dictionary['messages']
                        if rule['message_type'] == message_type), None)
        return next((transporter for transporter in message['valid_transports']
                     if transporter['format'] == message_format
                     and transporter['transport'] == message_transport), None)

    def get_all_messages(self, user):
        messages = self.get_messages_list(
            'northbound') + self.get_messages_list('southbound')
        messages = [msg for msg in messages
                    if msg in (user['data']['message_types']['northbound']
                               + user['data']['message_types']['southbound'])]
        messages = [msg + '-response' for msg in messages] + messages
        messages.sort()
        return messages

    def substitutes(self, message_type):
        message = next((rule for rule in self.rules_dictionary['messages']
                        if rule['message_type'] == message_type), None)
        if message:
            if 'substitute_paths' in message.keys():
                return message['substitute_paths']
            else:
                return
        else:
            return

    def sanitizers(self, message_type):
        message = next((rule for rule in self.rules_dictionary['messages']
                        if rule['message_type'] == message_type), None)
        if message:
            if 'sanitize_paths' in message.keys():
                return message['sanitize_paths']
            else:
                return
        else:
            return

    def sanitize_value(self, message_type, field_name, exception=False):
        message = next((rule for rule in self.rules_dictionary['messages']
                        if rule['message_type'] == message_type), None)
        if message:
            sanitizer_name = next((
                rule['sanitizer']
                for rule in message['sanitize_paths']
                if rule['field_name'] == field_name), None)
        else:
            sanitizer_name = None

        if sanitizer_name:
            sanitizer = next((
                rule
                for rule in self.rules_dictionary['sanitizers']
                if rule['name'] == sanitizer_name), None)

        else:
            sanitizer = None

        if sanitizer:
            return self.stub_element(sanitizer, exception)
        else:
            return None

    def stub_element(self, sanitizer, exception):
        new_id = str(uuid4())
        if not exception:
            payload = dict(sanitizer['creation_body'])
        else:
            payload = dict(sanitizer['exception_body'])
        to_replace = [key for key in payload.keys() if payload[key] == '*']
        for key in to_replace:
            payload[key] = new_id
        requests.post(
            self.app_config['DEV_FS_BASE_URL'] + sanitizer['creation_url'],
            json=payload,
            headers={'Authorization': 'Basic ' + self.app_config['FS_AUTH']},
            timeout=2
        )
        return new_id
