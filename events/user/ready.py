import user
import utils.log.logger as logger

@user.client.event
async def on_ready():
    logger.logger(log_method='success', log_message=f'Successfully connect to discord as user "{user.client.user.name}"')

