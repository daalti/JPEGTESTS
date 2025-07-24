import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 3Page_es_tt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:3Page-es_tt.obj=02ad66ef45fe88f43e18effb956aa64bdc6d2f6bf21ac20eead0e17a83a0cdd6
    +test_classification:System
    +name: test_pcl5_highvalue_3page_es_tt
    +test:
        +title: test_pcl5_highvalue_3page_es_tt
        +guid:7e7c00ff-5f63-4da6-9560-3fee7c9c6e97
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

def test_pcl5_highvalue_3page_es_tt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('02ad66ef45fe88f43e18effb956aa64bdc6d2f6bf21ac20eead0e17a83a0cdd6', timeout=600)
    outputsaver.save_output()
