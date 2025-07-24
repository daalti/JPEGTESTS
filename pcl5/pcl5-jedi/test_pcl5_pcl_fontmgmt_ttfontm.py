import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C51669549 pcl5 pcl using ttfontm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ttfontm.obj=c91a7dacf3e2b0e1c7d43a2c78db9179706c0835924198fdc152bafba8a822e6
    +test_classification:System
    +name: test_pcl5_pcl_fontmgmt_ttfontm
    +test:
        +title: test_pcl5_pcl_fontmgmt_ttfontm
        +guid:64f86196-087c-4ecc-827e-85a7326d59b1
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Home:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontmgmt_ttfontm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c91a7dacf3e2b0e1c7d43a2c78db9179706c0835924198fdc152bafba8a822e6', timeout=600)
    outputsaver.save_output()
