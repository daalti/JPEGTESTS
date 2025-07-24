import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 25Page_cursmovd.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:25Page-cursmovd.obj=abbffba262db94107a0b79dd5b90ee6ac7c4b912e407bbd177242f78b1bd58a4
    +test_classification:System
    +name: test_pcl5_highvalue_25page_cursmovd
    +test:
        +title: test_pcl5_highvalue_25page_cursmovd
        +guid:1d473167-3c9e-4e5d-925e-f9a32f312518
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_25page_cursmovd(setup_teardown, printjob, outputsaver):
    printjob.print_verify('abbffba262db94107a0b79dd5b90ee6ac7c4b912e407bbd177242f78b1bd58a4', timeout=600)
    outputsaver.save_output()
