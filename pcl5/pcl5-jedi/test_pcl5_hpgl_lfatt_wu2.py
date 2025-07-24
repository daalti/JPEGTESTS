import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using wu2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:wu2.obj=81991e979dd883447bd6d403c9bb3ceb962ac2d35f9240e449ab7612ce6e3777
    +test_classification:System
    +name: test_pcl5_hpgl_lfatt_wu2
    +test:
        +title: test_pcl5_hpgl_lfatt_wu2
        +guid:855bbf71-2690-4965-a261-1c50e91c9580
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_lfatt_wu2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('81991e979dd883447bd6d403c9bb3ceb962ac2d35f9240e449ab7612ce6e3777', timeout=600)
    outputsaver.save_output()
