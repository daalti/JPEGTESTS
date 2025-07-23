import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job to verify invalid/negetive test case from *PwgPhOnly-InvalidBitsPerClr-2.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-InvalidBitsPerClr-2.pwg=87ca72410ac621753b7b42f1c5cecff6f4ba382507dabc954a83b808c45ae476
    +name:test_pwg_negative_ph_only_invalid_bits_per_color_2
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Negative
    +test:
        +title:test_pwg_negative_ph_only_invalid_bits_per_color_2
        +guid:98d8267c-d55e-4377-9679-8d7311029a48
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_negative_ph_only_invalid_bits_per_color_2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('87ca72410ac621753b7b42f1c5cecff6f4ba382507dabc954a83b808c45ae476', 'FAILED')
    outputsaver.save_output()
