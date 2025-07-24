import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 5Page_raster_clip.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:5Page-raster_clip.obj=5820a2257d7af9bf75c5cc84411a52b7128f27ccc69e34e2667abeda0e24b9d8
    +test_classification:System
    +name: test_pcl5_highvalue_5page_raster_clip
    +test:
        +title: test_pcl5_highvalue_5page_raster_clip
        +guid:2a03f8c6-3e70-4f2e-89ba-9a5d74c0f2dd
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_5page_raster_clip(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5820a2257d7af9bf75c5cc84411a52b7128f27ccc69e34e2667abeda0e24b9d8', timeout=600)
    outputsaver.save_output()
