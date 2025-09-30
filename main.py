from utils.preflight import config_initializer
import utils.config_helper as config_helper
import utils.logger as logger

def main():
    config_initializer.initialize_config()

    config_helper.set_value('discord_user_token', 'asdsa22334')
    logger.logger(log_method='success', log_message='this is a test')
    

if __name__ == "__main__":
    main()