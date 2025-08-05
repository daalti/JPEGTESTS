import pytest
import logging

from dunetuf.network.ipp.ipp_utils import update_ipp_datfile
from dunetuf.print.output.intents import Intents, VerticalContentAlignment

PRINT_JPEG_DIFFERENT_MARGINS_TEST_FILE_PATH = "/code/tests/print/pdl/ipp/attributes/10x12-none.test"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a JPEG file using attribute value different-margig-settings
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-121987
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:10x12-none.jpg=951b4d586d30e957de71338f6e9697bcd8cb0385137f6b513412a9891e9446d4
    +name:test_ipp_jpeg_different_margins_center
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_jpeg_different_margins_center
        +guid:2f7fc66a-4780-44d5-a572-24ed25d0d62a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_jpeg_different_margins_center(setup_teardown, printjob, outputverifier, tray):
    expected_vertical_alignment = VerticalContentAlignment.CENTER

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_JPEG_DIFFERENT_MARGINS_TEST_FILE_PATH)

    printjob.ipp_print(update_dat_file, '951b4d586d30e957de71338f6e9697bcd8cb0385137f6b513412a9891e9446d4')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_vertical_content_alignment(Intents.printintent, expected_vertical_alignment)
