class BaseConverter:
    """Base class for converters"""
    def __init__(self, input_path, output_path):
        """Intialize setup converter."""
        self.input_path = input_path
        self.output_path = output_path

    def convert(self):
        "Converts media to specified format/codec"
        raise NotImplementedError("This method should be implemented by subclasses.")
