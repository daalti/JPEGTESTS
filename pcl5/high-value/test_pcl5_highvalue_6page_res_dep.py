import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 6Page_res_dep.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:6Page-res_dep.obj=12589ce5ad6cef371071857dab149337e1f8aa14c9cf735a6e8cccaa490ba17e
    +test_classification:System
    +name: test_pcl5_highvalue_6page_res_dep
    +test:
        +title: test_pcl5_highvalue_6page_res_dep
        +guid:c145493c-5bad-47f6-9fc5-3bce1ced9249
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

def test_pcl5_highvalue_6page_res_dep(setup_teardown, printjob, outputsaver):
    printjob.print_verify('12589ce5ad6cef371071857dab149337e1f8aa14c9cf735a6e8cccaa490ba17e')
    outputsaver.save_output()
