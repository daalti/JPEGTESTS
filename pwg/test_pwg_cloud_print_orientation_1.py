import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PwgCloudPrint-Orientation-1.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-Orientation-1.pwg=acd1927984e9ed031fc4dac26cbd29112725a05e235b263aa31abdb2465c488c
    +name:test_pwg_cloud_print_orientation_1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_orientation_1
        +guid:d32eb387-3b97-4223-bea8-354ba25614e3
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_orientation_1(setup_teardown, printjob, outputsaver):
    outputsaver.operation_mode('TIFF')

    printjob.print_verify('acd1927984e9ed031fc4dac26cbd29112725a05e235b263aa31abdb2465c488c')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
