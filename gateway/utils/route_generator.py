class Route_generator:
    """
    Route_generator class generates routes for a given resource with parameters.
    
    Attributes:
        protocol (str): The protocol (http or https).
        domain (str): The domain name of the API server.
    """
    
    def __init__(self, protocol='http', domain='example.com'):
        """
        Initializes the Route_generator with protocol and domain.
        
        Args:
            protocol (str, optional): The protocol to use (default is 'http').
            domain (str, optional): The domain name (default is 'example.com').
        """
        self.protocol = protocol
        self.domain = domain
    
    def _validate_protocol(self, protocol):
        """
        Validates the protocol is either 'http' or 'https'.
        
        Args:
            protocol (str): The protocol to validate.
        
        Raises:
            ValueError: If protocol is not 'http' or 'https'.
        """
        if protocol.lower() not in ['http', 'https']:
            raise ValueError("Protocol must be either 'http' or 'https'.")
    
    def generate_route(self, resource_name, params=None):
        """
        Generates a route for a specific resource with optional parameters.
        
        Args:
            resource_name (str): The name of the resource.
            params (dict, optional): Parameters to include in the route as query strings.
        
        Returns:
            str: The generated route.
        """
        route = f"{self.protocol}://{self.domain}/{resource_name}"
        if params:
            route += '?' + '&'.join([f"{key}={value}" for key, value in params.items()])
        return route
