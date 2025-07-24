import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using rasheal.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:rasheal.obj=16bb2b8b86e3c6581ff833b62927cc897b3ddf6350b1c82b694e28e485960752
    +test_classification:System
    +name: test_pcl5_pcl_raster_rasheal
    +test:
        +title: test_pcl5_pcl_raster_rasheal
        +guid:6878c731-f5bb-4b5a-9152-a78626a3b405
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_raster_rasheal(setup_teardown, printjob, outputsaver):
    printjob.print_verify('16bb2b8b86e3c6581ff833b62927cc897b3ddf6350b1c82b694e28e485960752', timeout=600)
    outputsaver.save_output()
