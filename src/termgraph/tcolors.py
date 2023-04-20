class tcolors:
    """Class which contains various terminal color utilities."""
    PURPLE = '\033[95m'
    WHITE = '\033[37m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def c(color, term):
        """Helper method to apply a specific color to a piece of text."""
        return color + term + tcolors.ENDC

