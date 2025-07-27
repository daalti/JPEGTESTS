import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Erroneous PCL3GUI file fails successfully without crashes
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-140912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:cannot_be_canceled.prn=67a05f131f07edbabda1c0214f6eddad160e141780f376fc40dcbfe2b1ca97ba
    +name:test_pcl3_cannot_be_canceled
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3_cannot_be_canceled
        +guid:b9319731-53ad-481e-bfa3-17865e5e13fd
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL3GUI
    +overrides:
        +Home:
            +is_manual:False
            +timeout:240
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl3_cannot_be_canceled(setup_teardown, printjob, outputsaver):
    printjob.print_verify('67a05f131f07edbabda1c0214f6eddad160e141780f376fc40dcbfe2b1ca97ba')
    outputsaver.save_output()
