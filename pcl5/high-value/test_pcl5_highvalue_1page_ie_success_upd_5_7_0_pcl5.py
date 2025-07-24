import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_IE_Success_UPD_5_7_0_PCL5.prn
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:700
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:1Page-IE_-_Success_-_UPD_5.7.0_PCL5.prn=80da4594cb59be3e5f920be913762905b7fba8b931f6d5fc3a4571c9963f772d
    +test_classification:System
    +name: test_pcl5_highvalue_1page_ie_success_upd_5_7_0_pcl5
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_1page_ie_success_upd_5_7_0_pcl5
        +guid:7de1e60d-19e1-40cf-a27e-a74b373f91bd
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
def test_pcl5_highvalue_1page_ie_success_upd_5_7_0_pcl5(setup_teardown, printjob, outputsaver):
    printjob.print_verify('80da4594cb59be3e5f920be913762905b7fba8b931f6d5fc3a4571c9963f772d', timeout=600)
    outputsaver.save_output()
