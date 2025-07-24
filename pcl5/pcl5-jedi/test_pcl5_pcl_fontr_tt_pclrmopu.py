import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using pclrmopu.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pclrmopu.obj=e04e132f8d244aaf780aa7510729a819f9d5ceb241dd364f9cf913f3c1988918
    +test_classification:System
    +name: test_pcl5_pcl_fontr_tt_pclrmopu
    +test:
        +title: test_pcl5_pcl_fontr_tt_pclrmopu
        +guid:ab88ac92-ca52-4fa1-ab2f-f627a6d26dda
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontr_tt_pclrmopu(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e04e132f8d244aaf780aa7510729a819f9d5ceb241dd364f9cf913f3c1988918', timeout=600)
    outputsaver.save_output()
