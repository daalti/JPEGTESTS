import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 113Page_lo21.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1500
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:113Page-lo21.obj=9ae0a6055af4d69fabfcd671fb62056e1c7bd7c88f9569e8216e5c80d57fd803
    +test_classification:System
    +name: test_pcl5_highvalue_113page_lo21
    +test:
        +title: test_pcl5_highvalue_113page_lo21
        +guid:9873da1c-a6d0-45c7-acd0-e39836aa2828
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_113page_lo21(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9ae0a6055af4d69fabfcd671fb62056e1c7bd7c88f9569e8216e5c80d57fd803', timeout=1500)
    outputsaver.save_output()
