from .converter.converter import DataConverter, DataBundle, InputFile
from .metadata.metadata import MetadataBuilder, Metadata


class Manager:
    
    def __init__(self, folder_name: str, file_name: str):
        
        self.converter: DataConverter = DataConverter(InputFile(folder_name=folder_name, file_name=file_name))
        self.data_bundle: DataBundle | None = None
    

    
    # -------------------------------------------------------
    # Main pipeline entry point
    # -------------------------------------------------------
    def run(self) -> Manager:
        """Run the full process: load data → build metadata → bundle output."""

        
        self.data_bundle = self.converter.convert()
        
        
        
        
        

        # # 2. Build metadata (from converter.qme or info table)
        # metadata_builder = MetadataBuilder(self.converter.df_info)
        # self.metadata = metadata_builder.build()

        # # 3. Create DataBundle
        # self.bundle = DataBundle(
            
        #     df_data=self.converter.df_data,
        #     metadata=self.metadata,
        # )

        return self