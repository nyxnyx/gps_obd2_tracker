class BaseUpdater:
    """Base class for all components that can perform periodic updates."""
    
    def __init__(self, api_instance):
        self.api = api_instance

    async def update(self):
        """Perform the update action. Must be implemented by subclasses."""
        raise NotImplementedError()