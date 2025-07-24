import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_dirpix.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-dirpix.obj=5261cf34a9b0d6d44035fd5304b92a4282b971d02fc78f783f7a2fdcb5a05441
    +test_classification:System
    +name: test_pcl5_highvalue_1page_dirpix
    +test:
        +title: test_pcl5_highvalue_1page_dirpix
        +guid:d60e2ecc-5579-4896-a1da-84b171ce6e00
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

def test_pcl5_highvalue_1page_dirpix(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5261cf34a9b0d6d44035fd5304b92a4282b971d02fc78f783f7a2fdcb5a05441')
    outputsaver.save_output()
