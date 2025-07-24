import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 18Page_echo.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:18Page-echo.obj=e231078f97d6cc142d2e6a90da6dc60ccb485c0760727c6a77a1801d6127b527
    +test_classification:System
    +name: test_pcl5_highvalue_18page_echo
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_18page_echo
        +guid:dc4a3e57-968f-4ba0-9408-6ffed014b8ee
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

def test_pcl5_highvalue_18page_echo(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e231078f97d6cc142d2e6a90da6dc60ccb485c0760727c6a77a1801d6127b527')
    outputsaver.save_output()
