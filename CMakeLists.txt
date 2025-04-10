cmake_minimum_required(VERSION 3.13.4)

project(UpperAirwaySegmentator)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://github.com/alejandro-matos/SlicerUpperAirwaySegmentator")
set(EXTENSION_CATEGORY "Segmentation")
set(EXTENSION_CONTRIBUTORS "Alejandro Matos Camarillo (uAlberta), Silvia Capenakas (uAlberta)")
set(EXTENSION_DESCRIPTION "Fully automatic AI segmentation tool for upper airway CBCT scans based on UpperAirwaySegmentator nnU-Net model.")
set(EXTENSION_ICONURL "https://github.com/gaudot/SlicerUpperAirwaySegmentator/raw/main/UpperAirwaySegmentator/Resources/Icons/UpperAirwaySegmentator_full_icon.png")
set(EXTENSION_SCREENSHOTURLS "https://github.com/alejandro-matos/SlicerUpperAirwaySegmentator/raw/main/Screenshots/11.png")
set(EXTENSION_DEPENDS "NNUNet") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(UpperAirwaySegmentator)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
