import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 2Page_clip_coordsys.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:2Page-clip_coordsys.obj=27705d4558867a38616e6bb0849288b263f260f462e8296da1765b9c0e208bd6
    +test_classification:System
    +name: test_pcl5_highvalue_2page_clip_coordsys
    +test:
        +title: test_pcl5_highvalue_2page_clip_coordsys
        +guid:9b5eabad-32e0-4354-a634-6a693a8121d0
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

def test_pcl5_highvalue_2page_clip_coordsys(setup_teardown, printjob, outputsaver):
    printjob.print_verify('27705d4558867a38616e6bb0849288b263f260f462e8296da1765b9c0e208bd6', timeout=600)
    outputsaver.save_output()
