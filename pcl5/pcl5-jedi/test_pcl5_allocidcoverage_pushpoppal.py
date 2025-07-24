import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 allocidcoverage using pushPopPal.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pushPopPal.pcl=937f220f1a1cee3019ba499f0dca294c38a01e1bd11fb7336697daaadc359de1
    +test_classification:System
    +name: test_pcl5_allocidcoverage_pushpoppal
    +test:
        +title: test_pcl5_allocidcoverage_pushpoppal
        +guid:bb0a1ab6-0b67-4e92-9967-367692110f23
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_allocidcoverage_pushpoppal(setup_teardown, printjob, outputsaver):
    printjob.print_verify('937f220f1a1cee3019ba499f0dca294c38a01e1bd11fb7336697daaadc359de1', timeout=600)
    outputsaver.save_output()
