import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 8Page_pitch.obj
    +test_tier: 3
    +is_manual:False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:240
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:8Page-pitch.obj=e0dbf8061a911605b848d44231eeef2b17f998698cc203a4bb1880ad08ee949f
    +test_classification:System
    +name: test_pcl5_highvalue_8page_pitch
    +test:
        +title: test_pcl5_highvalue_8page_pitch
        +guid:08c157fd-ad08-459d-9e16-c5a3858ad474
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_8page_pitch(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e0dbf8061a911605b848d44231eeef2b17f998698cc203a4bb1880ad08ee949f',timeout=240)
    outputsaver.save_output()
