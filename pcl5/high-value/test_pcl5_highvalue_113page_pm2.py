import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 113Page_pm2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:3720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:113Page-pm2.obj=a278d4d950c1fdbc3be3bf3b3c908ca373a3b25bdcb27ab6ed4091685d29a189
    +test_classification:System
    +name: test_pcl5_highvalue_113page_pm2
    +test:
        +title: test_pcl5_highvalue_113page_pm2
        +guid:81da33b7-a1f5-478a-97c7-728839898031
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:3720
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_113page_pm2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a278d4d950c1fdbc3be3bf3b3c908ca373a3b25bdcb27ab6ed4091685d29a189', timeout=3600)
    outputsaver.save_output()
