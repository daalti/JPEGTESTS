import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pcl3Gui_DinA1_image_LocPort_Neptune_PCL3v4
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-18107
    +timeout:360
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:DinA1_image_LocPort_Neptune_PCL3v4.prn=d12c32dc8c21ab67365790c727bfc924722f4a7e590e7a1c44a7ea9ada089610
    +test_classification:System
    +name:test_pcl3Gui_DinA1_image_LocPort_Neptune_PCL3v4
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3Gui_DinA1_image_LocPort_Neptune_PCL3v4
        +guid:3150c546-347e-11eb-a8d4-37d9e301f901
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI & MediaSizeSupported=iso_a1_594x841mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl3Gui_DinA1_image_LocPort_Neptune_PCL3v4(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d12c32dc8c21ab67365790c727bfc924722f4a7e590e7a1c44a7ea9ada089610', timeout=300)
    outputsaver.save_output()

    logging.info("Pcl3Gui DinA1_image_LocPort_Neptune_PCL3v4- Print job completed successfully")
