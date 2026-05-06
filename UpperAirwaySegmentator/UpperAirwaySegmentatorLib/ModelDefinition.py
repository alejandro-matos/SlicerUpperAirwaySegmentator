class ModelDefinition:
    """
    Description of a selectable nnU-Net model.

    To add another trained model, add a new entry to MODEL_DEFINITIONS with a
    unique key, a display name, and either download_url or release_asset_name.
    """

    def __init__(
        self,
        key,
        display_name,
        repo_path="alejandro-matos/SlicerUpperAirwaySegmentator",
        release_asset_name=None,
        download_url=None,
    ):
        self.key = key
        self.display_name = display_name
        self.repo_path = repo_path
        self.release_asset_name = release_asset_name
        self.download_url = download_url


MODEL_DEFINITIONS = (
    ModelDefinition(
        key="upper_airway_155cbct",
        display_name="Upper airway with sinuses",
        release_asset_name="Dataset014_Airways_155CBCT_fold_all.zip",
    ),
    # Add your second trained model here. Example:
    ModelDefinition(
        key="Dataset001_Airways_Fink",
        display_name="Upper airway no sinuses",
        release_asset_name="Dataset001_Airways_Fink.zip",
    ),
)
