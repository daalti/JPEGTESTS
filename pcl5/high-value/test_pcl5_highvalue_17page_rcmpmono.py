import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 17Page_rcmpmono.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:17Page-rcmpmono.obj=663c137fbf0db950d99328480c7d34c673fe7c721b172168ffb282dad3825f35
    +test_classification:System
    +name: test_pcl5_highvalue_17page_rcmpmono
    +test:
        +title: test_pcl5_highvalue_17page_rcmpmono
        +guid:1ac86b43-0b98-4e2f-a2b0-0b944287f81b
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

def test_pcl5_highvalue_17page_rcmpmono(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('663c137fbf0db950d99328480c7d34c673fe7c721b172168ffb282dad3825f35',timeout=600)
    outputsaver.save_output()
