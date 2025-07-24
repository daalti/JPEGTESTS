import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_indxpix.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-indxpix.obj=fa01d9ff1cd5378fce1cf7dedb3061eba4df708c01df06692997e19f632354f0
    +test_classification:System
    +name: test_pcl5_highvalue_1page_indxpix
    +test:
        +title: test_pcl5_highvalue_1page_indxpix
        +guid:1295866a-5580-41f2-b9b7-9cf4193204e9
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

def test_pcl5_highvalue_1page_indxpix(setup_teardown, printjob, outputsaver):
    printjob.print_verify('fa01d9ff1cd5378fce1cf7dedb3061eba4df708c01df06692997e19f632354f0', timeout=600)
    outputsaver.save_output()
