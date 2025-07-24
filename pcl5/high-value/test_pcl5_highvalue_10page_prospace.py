import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 10Page_prospace.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:400
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:10Page-prospace.obj=67ae3cada79c614048977f79d6b8f8c6c7af5318e0817d678f37d120a1e61929
    +test_classification:System
    +name: test_pcl5_highvalue_10page_prospace
    +test:
        +title: test_pcl5_highvalue_10page_prospace
        +guid:225364d0-e6ea-4c7d-b806-66261a26b14f
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
def test_pcl5_highvalue_10page_prospace(setup_teardown, printjob, outputsaver):
    printjob.print_verify('67ae3cada79c614048977f79d6b8f8c6c7af5318e0817d678f37d120a1e61929', timeout=400)
    outputsaver.save_output()
