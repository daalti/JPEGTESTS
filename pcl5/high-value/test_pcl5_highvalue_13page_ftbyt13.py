import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 13Page_ftbyt13.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:13Page-ftbyt13.obj=d9dec81c727ef6d86eb3492b4a65ab06df7a1327e4aac9bcd1e87c6171dc71d4
    +test_classification:System
    +name: test_pcl5_highvalue_13page_ftbyt13
    +test:
        +title: test_pcl5_highvalue_13page_ftbyt13
        +guid:b77c812b-27b0-43a1-a3ff-7ba90842e654
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

def test_pcl5_highvalue_13page_ftbyt13(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d9dec81c727ef6d86eb3492b4a65ab06df7a1327e4aac9bcd1e87c6171dc71d4', timeout=300)
    outputsaver.save_output()
