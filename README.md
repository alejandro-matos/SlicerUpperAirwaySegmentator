# Slicer UpperAirwaySegmentator 

3D Slicer extension for fully-automatic segmentation of CBCT upper airway volumes using "UpperAirwaySegmentator"

<img src="https://github.com/alejandro-matos/SlicerUpperAirwaySegmentator/raw/main/Screenshots/11.png" width="700"/>

## UpperAirwaySegmentator Model
UpperAirwaySegmentator is built on the nnUNet framework and segments the pharyngeal and sinonasal airway regions. The dataset was split 70:30 into training and testing sets and included 75 CBCT scans from the University of Alberta, 65 from a private Chilean center, and 80 CT scans (40 pre- and 40 post-operative) from surgical departments in France.

If you use UpperAirwaySegmentator for your work, please also cite <!--our paper and -->nnU-Net:

<!-- Matos Camarillo A, Capenakas-Gianoni S, Punithakumar K, Lagravere-Vich M. AirwaySegmentator: A deep learning-based method for Nasopharyngeal airway segmentation. Published online Month day, 2024:2024.xx.xx.xxxxxxxx. doi:10.1101/2024.xx.xx.xxxxxxxx-->

> Isensee F, Jaeger PF, Kohl SAA, Petersen J, Maier-Hein KH. nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation. Nat Methods. 2021;18(2):203-211. doi:10.1038/s41592-020-01008-z
<img src="https://github.com/alejandro-matos/SlicerUpperAirwaySegmentator/raw/main/Screenshots/angles.png" width="500"/>

## Using the extension

<!--[Here is a video tutorial](https://www.youtube.com/watch?v=BEG-XhjjiaY) showing the installation process and demonstrating the main capabilities of the extension.-->

This extension is compatible with the 3D Slicer Preview Release (version 5.7.0, or later), downloadable [from the official website]( https://download.slicer.org/ ). 

<!--The extension is not yet available in the extension manager as of October 21, 2024. Thus, it is necessary to install the extension manually by downloading it to your computer and using the extension wizard, similarly as how it is shown in this [video tutorial]([https://youtu.be/QsxzjQb05D4?si=haksYNjVlO9nJO8l&t=78]))-->

The plugin can be installed in Slicer using the [extension manager]( https://slicer.readthedocs.io/en/latest/user_guide/extensions_manager.html#install-extensions).
It can be found using the search bar by typing "UpperAirwaySegmentator".

<img src="https://github.com/alejandro-matos/SlicerUpperAirwaySegmentator/raw/main/Screenshots/5.png" width="500"/>

After the install process and restart of Slicer, the extension can be found in the module file explorer under `Segmentation>UpperAirwaySegmentator`.
It can also be found by using the `find` module button and searching for the keyword `UpperAirwaySegmentator`.

To use the extension, load a dental CT or CBCT by either drag and dropping the data in 3D Slicer or by using the
`DATA` or `DCM` load buttons.

<!--To test the extension, you can use 3D Slicer's `CBCT Dental Surgery` volumes. These volumes can be found in the
`Sample Data` module. -->

After loading the data, the data will be displayed in the 2D views.
Switch module to the `UpperAirwaySegmentator` module and select the volume in the first drop down menu.
Choose the trained AI model to use from the `AI model` drop down menu.

Click on the `Apply` button to start the segmentation.

<img src="https://github.com/alejandro-matos/SlicerUpperAirwaySegmentator/raw/main/Screenshots/4.png" width="500" />

During the first launch, the module's dependencies will be installed. These dependencies include : 
* The AI model weights
* Light the torch
* PyTorch
* nnUNet V2 

After the install, the volume will be transferred and sent to the nnUNet V2 library for processing.
If your device doesn't include CUDA, the processing may be very long and a dialog will ask for confirmation before
starting the segmentation process.

<img src="https://github.com/alejandro-matos/SlicerUpperAirwaySegmentator/raw/main/Screenshots/upperairwaysegmentator_run.gif"/>

During execution, the processing can be canceled using the `Stop` button.
The progress will be reported in the console logs.

<img src="https://github.com/alejandro-matos/SlicerUpperAirwaySegmentator/raw/main/Screenshots/5.png" width="500"/>

After the segmentation process has run, the segmentation will be loaded into the application.
The segmentation results can be modified using the `Segment Editor` tools.

<img src="https://github.com/alejandro-matos/SlicerUpperAirwaySegmentator/raw/main/Screenshots/upperairwaysegmentator_3dmodel.gif"/>

The segmentation can be exported as STL, NIfTI and/or OBJ using the `Export segmentation` menu and selecting the export format(s).

The `Surface smoothing` slider allows to change the 3D view surface smoothing algorithm.

<img src="https://github.com/alejandro-matos/SlicerUpperAirwaySegmentator/raw/main/Screenshots/6.png" width="500"/>

## Troubleshooting

### MacOS GPU acceleration

Due to an ongoing issue with Mac devices and Pytorch, GPU acceleration is not available for now on those devices.

### Linux Processing hang

On Linux or WSL system, the inference can get stuck at the stage : "done with volume".
This indicates that the process has run out of memory. 32 GB of RAM is recommended to run this extension. If you run 
into this issue, you can create a SWAP file on SSD with 16 GB which should solve the problem.

### Torch CUDA not properly installed

On Windows, the torch CUDA dependency may not properly be detected and installed.

To solve this problem, you can use the `PyTorch Utils` extension, uninstall the version of PyTorch and install 
a new version of PyTorch by setting the `Computation backend` compatible with your hardware. Make sure to restart Slicer after performing the re-installation.

The PyTorch version should be greater than `2.0.0` for nnUNet compatibility.

<img src="https://github.com/alejandro-matos/SlicerUpperAirwaySegmentator/raw/main/Screenshots/7.png" width="500"/>

### Failed to download / find weights

If the weights are not correctly installed, you can install them manually.
To do so, go to https://github.com/alejandro-matos/SlicerUpperAirwaySegmentator  and select the latest release.

Download the latest `.zip` file from the release.

Navigate to your `UpperAirwaySegmentator` folder (this folder can be also found in the module finder window).

<!-- <img src="https://github.com/alejandro-matos/SlicerUpperAirwaySegmentator/raw/main/Screenshots/8.png" width="500"/> -->

Unzip the weight file in the model-specific folder under `UpperAirwaySegmentator\Resources\ML`.
For example, the default model is stored in `UpperAirwaySegmentator\Resources\ML\upper_airway_155cbct`.

Create a `download_info.json` file containing the path to the downloaded zip file for future reference : 

{
  "download_url": "https://github.com/alejandro-matos/SlicerUpperAirwaySegmentator/releases/download/v1.0.0-alpha/Dataset014_Airways_155CBCT_fold_all.zip "
}

### Adding another trained model

Selectable models are defined in `UpperAirwaySegmentator/UpperAirwaySegmentatorLib/ModelDefinition.py`.
Add one `ModelDefinition` per trained model:

```python
ModelDefinition(
    key="upper_airway_second_model",
    display_name="Upper airway second model",
    release_asset_name="DatasetXXX_YourSecondModel.zip",
)
```

The `key` becomes the local weights folder name under `Resources/ML`.
The `display_name` is shown in the Slicer module.
Use `release_asset_name` when the weights are attached to a GitHub release, or `download_url` when you want to point directly to a `.zip` file.

### Failed to load segmentation

Error reads "Failed to load segmentation. Something went wrong during nnUNet processing. Please check the logs for potential errors and contact the library maintainers." Check that the Torch version is at least 2.0.0.
Otherwise, try uninstalling the PyTorch extension, restart 3D Slicer, and then reinstall the PyTorch extension again.

## Contributing

This project welcomes contributions. If you want more information about how you can contribute, please refer to
the [CONTRIBUTING.md file](CONTRIBUTING.md).

## Acknowledgments 

Authors: A. Matos Camarillo (University of Alberta), S. Capenakas-Gianoni (University of Alberta), K. Punithakumar (University of Alberta), M. Lagravere-Vich (University of Alberta)

<!-- Supported by the [tk Add source of funding here] -->

This project references the structural framework of the [Slicer DentalSegmentator project](https://github.com/gaudot/SlicerDentalSegmentator/tree/main) extension, licensed under the Apache 2.0 License. Our implementation features independently trained models and custom modifications while maintaining attribution to the original structural framework.
<!-- ### Changes Made

- Incorporated our nnUNet-v2 model weights trained on the segmentation of the pharyngeal and sinonasal airway regions
- Details about new features or functionalities added.
- Any other relevant modifications. -->

## Contact

For clinical support:
Dr. Silvia Gianoni-Capenakas - capenaka@ualberta.ca,
Dr. Manuel Lagravere-Vich - manuel@ualberta.ca

For technical inquiries:
Alejandro Matos Camarillo - amatos@ualberta.ca
