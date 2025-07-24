import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 16Page_ctulineb.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:16Page-ctulineb.obj=f5b552ec0a09864ab6787870094b8a6c63d4e09b03ced7574338f937e9e2fcd3
    +test_classification:System
    +name: test_pcl5_highvalue_16page_ctulineb
    +test:
        +title: test_pcl5_highvalue_16page_ctulineb
        +guid:00ea071d-2f08-42d9-a2cc-99bdd2b33710
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

def test_pcl5_highvalue_16page_ctulineb(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('f5b552ec0a09864ab6787870094b8a6c63d4e09b03ced7574338f937e9e2fcd3',timeout=600)
    outputsaver.save_output()
