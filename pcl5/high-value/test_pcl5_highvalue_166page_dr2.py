import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 166Page_dr2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:3600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:166Page-dr2.obj=d38146e4e33c6c33fac98cb0073ed2e4247d06b4dc5892079058181f04252265
    +test_classification:System
    +name: test_pcl5_highvalue_166page_dr2
    +test:
        +title: test_pcl5_highvalue_166page_dr2
        +guid:9e20b44b-f8e6-4ca8-a4a0-e79ca478b390
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

def test_pcl5_highvalue_166page_dr2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d38146e4e33c6c33fac98cb0073ed2e4247d06b4dc5892079058181f04252265', timeout=3600)
    outputsaver.save_output()
