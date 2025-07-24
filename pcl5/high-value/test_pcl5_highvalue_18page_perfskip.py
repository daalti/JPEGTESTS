import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 18Page_perfskip.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:18Page-perfskip.obj=6f65d87d8f5b55325f0dc9a6881face773c4be2f84f826b960f4bfb5d6280c7d
    +test_classification:System
    +name: test_pcl5_highvalue_18page_perfskip
    +test:
        +title: test_pcl5_highvalue_18page_perfskip
        +guid:b0741eb7-2809-49cc-bd2a-496bae66fc75
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

def test_pcl5_highvalue_18page_perfskip(setup_teardown, printjob, outputsaver):
    printjob.print_verify('6f65d87d8f5b55325f0dc9a6881face773c4be2f84f826b960f4bfb5d6280c7d',timeout=600)
    outputsaver.save_output()
