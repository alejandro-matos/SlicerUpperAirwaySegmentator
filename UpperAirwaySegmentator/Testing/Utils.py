import unittest
from pathlib import Path
import json
import os
from UpperAirwaySegmentatorLib import MODEL_DEFINITIONS, SegmentationWidget

import slicer


class UpperAirwaySegmentatorTestCase(unittest.TestCase):
    def setUp(self):
        self._clearScene()

        # Get the path to the ML folder
        ml_folder = Path(SegmentationWidget.nnUnetFolder(MODEL_DEFINITIONS[0].key))
        
        # Create the directory if it doesn't exist
        os.makedirs(ml_folder, exist_ok=True)
        
        # Create the download_info.json file
        download_info = {
            "download_url": "https://github.com/alejandro-matos/SlicerUpperAirwaySegmentator/releases/download/v1.0.1/Dataset014_Airways_155CBCT_fold_all.zip"
        }
        
        with open(ml_folder / "download_info.json", "w") as f:
            json.dump(download_info, f)

        with open(ml_folder / "dataset.json", "w") as f:
            json.dump({}, f)

    @staticmethod
    def _clearScene():
        slicer.app.processEvents()
        slicer.mrmlScene.Clear()
        slicer.app.processEvents()

    def tearDown(self):
        slicer.app.processEvents()


def _dataFolderPath():
    return Path(__file__).parent.joinpath("Data")


def load_test_CT_volume():
    import SampleData
    SampleData.SampleDataLogic().downloadDentalSurgery()
    return list(slicer.mrmlScene.GetNodesByName("PreDentalSurgery"))[0]


def get_test_label_path():
    return _dataFolderPath().joinpath("UpperAirway_Segmentation.nii.gz").as_posix()
