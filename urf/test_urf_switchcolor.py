import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **SwitchColor.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:SwitchColor.urf=a445610a2c3d101855f4ef2256cb07d7e274b5d19858839eeacbc4700f8becc2
    +name:test_urf_switchcolor
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_switchcolor
        +guid:c98c0e4e-b59d-46d0-a71c-0a9e415a6bdb
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF
    +overrides:
        +Home:
            +is_manual:False
            +timeout:360
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_switchcolor(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a445610a2c3d101855f4ef2256cb07d7e274b5d19858839eeacbc4700f8becc2')
    outputsaver.save_output()
