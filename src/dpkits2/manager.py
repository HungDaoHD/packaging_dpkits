from .converter.converter import DataConverter, InputFile
from .databox.databox import DataBox



class Manager:
    
    def __init__(self, folder_name: str, file_name: str):
        
        self.converter: DataConverter = DataConverter(InputFile(folder_name=folder_name, file_name=file_name))
        self.data_box: DataBox | None = None

    
    
    # -------------------------------------------------------
    # Main pipeline entry point
    # -------------------------------------------------------
    def run(self) -> Manager:
        """Run the full process: load data → build metadata → bundle output."""
        self.data_box = self.converter.convert()
        return self
    
    
    
    # -------------------------------------------------------
    # Convenience Accessors
    # -------------------------------------------------------
    @property
    def data(self):
        """Return cleaned / processed dataframe."""
        if not self.data_box:
            raise RuntimeError("Manager has not been run yet.")
        return self.data_box.df_data
    


    @property
    def qres(self):
        """Shortcut to metadata question structure."""
        if not self.data_box.metadata:
            raise RuntimeError("Metadata not built yet.")
        return self.data_box.metadata.qres

    
    
    def metadata_to_json(self, full_path: str):
        """Shortcut to save metadata as json files"""
        if not self.data_box.metadata:
            raise RuntimeError("Metadata not built yet.")
        
        self.data_box.metadata.save_json(filepath=full_path)