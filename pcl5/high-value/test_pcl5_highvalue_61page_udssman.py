import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 61Page_udssman.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1200
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:61Page-udssman.obj=fc3ce38fb38b0f1f2343bcdf3afbe8b18e73ea95a39c7ef751e7f54acb3dbb29
    +test_classification:System
    +name: test_pcl5_highvalue_61page_udssman
    +test:
        +title: test_pcl5_highvalue_61page_udssman
        +guid:d3241b83-d8b3-4492-9320-477d74ec1d74
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

def test_pcl5_highvalue_61page_udssman(setup_teardown, printjob, outputsaver):
    printjob.print_verify('fc3ce38fb38b0f1f2343bcdf3afbe8b18e73ea95a39c7ef751e7f54acb3dbb29', timeout=1200)
    outputsaver.save_output()
