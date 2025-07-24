import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 218Page_pfsclfct2.obj
    +test_tier: 3
    +is_manual:False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:3600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:218Page-pfsclfct2.obj=0e2f21b1f48e0a3a3f268cdf4c704d7efdea670e8a9206444197ace53e6de10a
    +test_classification:System
    +name: test_pcl5_highvalue_218page_pfsclfct2
    +test:
        +title: test_pcl5_highvalue_218page_pfsclfct2
        +guid:532e0a08-7f94-4590-9b81-88bc9af67963
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_218page_pfsclfct2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('0e2f21b1f48e0a3a3f268cdf4c704d7efdea670e8a9206444197ace53e6de10a', timeout=3600)
    outputsaver.save_output()
