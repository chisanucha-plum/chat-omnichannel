from model.configuration import Configuration as SystemConfiguration

class LineService():
    """
    Line service to handle line-related operations.
    """
    
    def __init__(self, oa_user_id: str) -> None:
        config = SystemConfiguration.get_config()
        
        channels = config.channels
        
        for channel in channels:
            if channel.user_id == oa_user_id:
                self.channel = channel