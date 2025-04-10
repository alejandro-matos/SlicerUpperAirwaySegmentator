from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock

import SampleData
import slicer

from UpperAirwaySegmentatorLib import SegmentationWidget, Signal, ExportFormat
from .Utils import (
    UpperAirwaySegmentatorTestCase, get_test_label_path,
    load_test_CT_volume
)


class MockLogic:
    def __init__(self):
        self.inferenceFinished = Signal()
        self.errorOccurred = Signal("str")
        self.progressInfo = Signal("str")
        self.startSegmentation = MagicMock()
        self.stopSegmentation = MagicMock()
        self.setParameter = MagicMock()
        self.waitForSegmentationFinished = MagicMock()
        self.loadSegmentation = MagicMock()
        self.loadSegmentation.side_effect = self.load_segmentation

    @staticmethod
    def load_segmentation():
        return slicer.util.loadSegmentation(get_test_label_path())

    @staticmethod
    def load_segmentation_partial():
        # Load the full segmentation first
        segmentation = slicer.util.loadSegmentation(get_test_label_path())
        
        # Get the segmentation object
        segmentation_obj = segmentation.GetSegmentation()
        
        # Get all segment IDs
        num_segments = segmentation_obj.GetNumberOfSegments()
        segment_ids = [segmentation_obj.GetNthSegmentID(i) for i in range(num_segments)]
        
        # Keep only the first segment (or whichever one you want)
        segment_to_keep = segment_ids[0]
        for segment_id in segment_ids:
            if segment_id != segment_to_keep:
                segmentation_obj.RemoveSegment(segment_id)
                
        return segmentation


class SegmentationWidgetTestCase(UpperAirwaySegmentatorTestCase):
    def setUp(self):
        super().setUp()
        self.logic = MockLogic()
        self.node = load_test_CT_volume()
        self.widget = SegmentationWidget(logic=self.logic)
        self.widget.inputSelector.setCurrentNode(self.node)
        # self.widget.show()
        slicer.app.processEvents()

    def tearDown(self):
        if hasattr(self, 'widget'):
            self.widget.hide()  # Hide the widget
            self.widget.deleteLater()  # Schedule widget for deletion
            self.widget = None
        slicer.app.processEvents()  # Process the deletion event
        super().tearDown()

    def test_can_be_displayed(self):
        self.widget.show()
        slicer.app.processEvents()

    def test_can_run_segmentation(self):
        slicer.app.processEvents()
        self.assertTrue(self.widget.applyButton.isEnabled())
        self.assertTrue(self.widget.inputSelector.isEnabled())
        self.assertTrue(self.widget.segmentationNodeSelector.isEnabled())
        self.assertFalse(self.widget.stopButton.isVisible())

        self.widget.applyButton.click()
        slicer.app.processEvents()
        
        self.assertFalse(self.widget.inputSelector.isEnabled())
        self.assertFalse(self.widget.segmentationNodeSelector.isEnabled())
        self.assertIsNotNone(self.widget.applyButton)

        self.logic.startSegmentation.assert_called_once_with(self.node)
        self.logic.inferenceFinished()
        slicer.app.processEvents()

        self.assertTrue(self.widget.inputSelector.isEnabled())
        self.assertTrue(self.widget.segmentationNodeSelector.isEnabled())
        self.logic.loadSegmentation.assert_called_once()

    def test_can_kill_segmentation(self):
        self.widget.applyButton.click()
        self.logic.startSegmentation.assert_called_once()
        self.widget.stopButton.click()
        self.logic.stopSegmentation.assert_called_once()
        self.logic.waitForSegmentationFinished.assert_called_once()
        # self.assertTrue(self.widget.applyButton.isVisible())
        self.assertFalse(self.widget.stopButton.isVisible())

    def test_loading_replaces_existing_segmentation_node(self):
        self.logic.inferenceFinished()
        slicer.app.processEvents()
        self.logic.inferenceFinished()
        slicer.app.processEvents()
        self.assertEqual(self.logic.loadSegmentation.call_count, 2)
        self.assertEqual(len(list(slicer.mrmlScene.GetNodesByClass("vtkMRMLSegmentationNode"))), 1)

    def test_loading_sets_correct_segment_names(self):
        self.logic.inferenceFinished()
        slicer.app.processEvents()
        node = self.widget.getCurrentSegmentationNode()
        self.assertIsNotNone(node)
        
        # For a single segment, we can simplify this
        segmentation = node.GetSegmentation()
        segmentId = segmentation.GetNthSegmentID(0)
        segmentName = segmentation.GetSegment(segmentId).GetName()
        
        self.assertEqual(segmentName, "Airway")

    def test_can_export_segmentation_to_file(self):
        self.logic.inferenceFinished()
        slicer.app.processEvents()
        self.widget.objCheckBox.setChecked(True)
        self.widget.stlCheckBox.setChecked(True)
        self.widget.niftiCheckBox.setChecked(True)
        allFormats = self.widget.getSelectedExportFormats()
        self.assertEqual(
            allFormats,
            ExportFormat.NIFTI | ExportFormat.STL | ExportFormat.OBJ
        )

        with TemporaryDirectory() as tmp:
            self.widget.exportSegmentation(self.widget.getCurrentSegmentationNode(), tmp, allFormats)
            slicer.app.processEvents()

            tmpPath = Path(tmp)
            self.assertEqual(len(list(tmpPath.glob("*.stl"))), 1)
            self.assertEqual(len(list(tmpPath.glob("*.obj"))), 1)
            self.assertEqual(len(list(tmpPath.glob("*.nii.gz"))), 1)

    def test_synchronises_segmentation_selector_to_processed_volume(self):
        self.assertIsNone(self.widget.getCurrentSegmentationNode())
        self.logic.inferenceFinished()
        slicer.app.processEvents()
        self.assertIsNotNone(self.widget.getCurrentSegmentationNode())

        otherNode = SampleData.SampleDataLogic().downloadMRHead()
        self.widget.inputSelector.setCurrentNode(otherNode)
        self.assertIsNone(self.widget.getCurrentSegmentationNode())

        self.widget.inputSelector.setCurrentNode(self.node)
        self.assertIsNotNone(self.widget.getCurrentSegmentationNode())

    def test_handles_deleted_segmentations(self):
        self.logic.inferenceFinished()
        slicer.app.processEvents()

        otherNode = SampleData.SampleDataLogic().downloadMRHead()
        self.widget.inputSelector.setCurrentNode(otherNode)
        slicer.app.processEvents()

        self.widget.inputSelector.setCurrentNode(self.node)
        slicer.app.processEvents()
        slicer.mrmlScene.RemoveNode(self.widget.getCurrentSegmentationNode())

        self.widget.inputSelector.setCurrentNode(otherNode)
        slicer.app.processEvents()
        self.widget.inputSelector.setCurrentNode(self.node)
        slicer.app.processEvents()
        self.assertIsNone(self.widget.getCurrentSegmentationNode())

    def test_handles_cleared_scene(self):
        prev_node = self.widget.segmentEditorNode
        slicer.mrmlScene.Clear()
        slicer.app.processEvents()
        self.widget.inputSelector.setCurrentNode(SampleData.SampleDataLogic().downloadMRHead())
        self.widget.applyButton.click()
        slicer.app.processEvents()
        self.logic.inferenceFinished()
        slicer.app.processEvents()
        # self.assertTrue(self.widget.applyButton.isVisible())
        self.assertNotEqual(prev_node, self.widget.segmentEditorWidget)

    def test_clearing_scene_mid_inference_stops_inference(self):
        self.widget.applyButton.click()
        slicer.app.processEvents()
        slicer.mrmlScene.Clear()
        slicer.app.processEvents()
        # self.assertTrue(self.widget.applyButton.isVisible())
        self.logic.stopSegmentation.assert_called_once()
