import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using indxpicYoffset.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:indxpicYoffset.pcl=f9fa4eea332197636b411fb3a3d740b4ec57185667a0cf6219a2db0582c36838
    +test_classification:System
    +name: test_pcl5_testfiles_raster_indxpicyoffset
    +test:
        +title: test_pcl5_testfiles_raster_indxpicyoffset
        +guid:6640d9b6-9295-4193-a50a-d8e3004bd6d9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_raster_indxpicyoffset(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f9fa4eea332197636b411fb3a3d740b4ec57185667a0cf6219a2db0582c36838', timeout=600)
    outputsaver.save_output()
