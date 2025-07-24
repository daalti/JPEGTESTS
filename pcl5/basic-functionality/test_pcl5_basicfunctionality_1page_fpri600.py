import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 1Page_fpri600.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-fpri600.obj=980cabbf08033824f1375b2ffc25963578d63833a42e3a1d20321495d35186b4
    +test_classification:System
    +name: test_pcl5_basicfunctionality_1page_fpri600
    +test:
        +title: test_pcl5_basicfunctionality_1page_fpri600
        +guid:a0cc1845-8f28-4fe8-a6b9-559feef54e08
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_basicfunctionality_1page_fpri600(setup_teardown, printjob, outputsaver):
    printjob.print_verify('980cabbf08033824f1375b2ffc25963578d63833a42e3a1d20321495d35186b4')
    outputsaver.save_output()
