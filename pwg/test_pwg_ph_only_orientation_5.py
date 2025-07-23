import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PwgPhOnly-Orientation-5.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-Orientation-5.pwg=e8d6eb113131fbb8a30b9e0f63ef61f4b158c5151550c0111b023797204eabf1
    +name:test_pwg_ph_only_orientation_5
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_orientation_5
        +guid:8eacfd80-d854-4b76-80b0-7f3c7f6121c7
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_orientation_5(setup_teardown, printjob, outputsaver):
    outputsaver.operation_mode('TIFF')

    printjob.print_verify('e8d6eb113131fbb8a30b9e0f63ef61f4b158c5151550c0111b023797204eabf1')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
