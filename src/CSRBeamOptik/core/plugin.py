
class CSRBeamOptik:

    """Interface for a online control plugin."""

    def __init__(self, session, settings):

    def connect(self):
        """Connect the online plugin to the control system."""

    def disconnect(self):
        """Unload the online plugin, free resources."""

    def execute(self):
        """Commit transaction."""

    def param_info(self, knob):
        """Get parameter info for backend key."""
        
        
    def read_monitor(self, name):
        """
        Read out one monitor, return values as dict with keys:

            widthx:     Beam x width
            widthy:     Beam y width
            posx:       Beam x position
            posy:       Beam y position
        """
        raise NotImplementedError

    def read_params(self, param_names=None):
        """Read all specified params (by default all). Return dict."""

    def read_param(self, param):
        """Read parameter. Return numeric value."""

    def write_param(self, param, value):
        """Update parameter into control system."""
        raise NotImplementedError
    
    def get_beam(self):
        """
        Return a dict ``{name: value}`` for all beam properties, in MAD-X
        units. At least: particle, mass, charge, energy
        """
        raise NotImplementedError

ParamInfo = namedtuple('ParamInfo', [
    'name',
    'ui_name',
    'ui_hint',
    'ui_prec',
    'unit',
    'ui_unit',
    'ui_conv',
])
