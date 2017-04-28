import configparser

config = configparser.ConfigParser()
config.read('config.cfg')
server = config.get('main', 'server')
wallet = config.get('main', 'wallet')
wallet_password = config.get('main', 'wallet_password')