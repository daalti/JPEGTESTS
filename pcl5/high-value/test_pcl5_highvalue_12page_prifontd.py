import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 12Page_prifontd.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:12Page-prifontd.obj=444ffd3c2936b2c4b0004591ebcbb0c2db16429ab0a6857f23584cd66931b95b
    +test_classification:System
    +name: test_pcl5_highvalue_12page_prifontd
    +test:
        +title: test_pcl5_highvalue_12page_prifontd
        +guid:89c150bb-0e3f-4fd9-b3a8-004cf09d693b
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

def test_pcl5_highvalue_12page_prifontd(setup_teardown, printjob, outputsaver):
    printjob.print_verify('444ffd3c2936b2c4b0004591ebcbb0c2db16429ab0a6857f23584cd66931b95b', timeout=300)
    outputsaver.save_output()
