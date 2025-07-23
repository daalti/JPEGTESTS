import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg letter 600x8 color four page duplex from *letter-600x8-color-4p-dup.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:letter-600x8-color-4p-dup.pwg=4046086f1d4058c9519db5d3f32832267305664c66e8c825f1a7b2f179427fdc
    +name:test_pwg_letter_600x8_color_four_page_duplex
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_letter_600x8_color_four_page_duplex
        +guid:bd7e2682-d02e-4c6d-a601-d8307078e992
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_letter_600x8_color_four_page_duplex(setup_teardown, printjob, outputsaver):
    outputsaver.operation_mode('TIFF')

    printjob.print_verify('4046086f1d4058c9519db5d3f32832267305664c66e8c825f1a7b2f179427fdc')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')

    logging.info("PWG Letter 600x8 Color Four Page Duplex - Print job completed successfully!")
