import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 49Page_rf_ct.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:49Page-rf_ct.obj=abda44fb9281cb50172aa7e44e66c6bf41fb486aed55367439b2e4bfff5ca695
    +test_classification:System
    +name: test_pcl5_highvalue_49page_rf_ct
    +test:
        +title: test_pcl5_highvalue_49page_rf_ct
        +guid:1788cbed-d4d8-429e-bf6d-8c3ba27fbfb1
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

def test_pcl5_highvalue_49page_rf_ct(setup_teardown, printjob, outputsaver):
    printjob.print_verify('abda44fb9281cb50172aa7e44e66c6bf41fb486aed55367439b2e4bfff5ca695', timeout=600)
    outputsaver.save_output()
