import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg a4 600x8 color one page from *a4-600x8-color-1p-sim.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:a4-600x8-color-1p-sim.pwg=a1ebe561325c2b4764cb55cbfdde3a3ed7907bd44f16760ee34523d7861a2a1a
    +name:test_pwg_a4_600x8_color_one_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_a4_600x8_color_one_page
        +guid:86ddacf8-b92d-428d-8be1-df4cb7f7ace2
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_a4_600x8_color_one_page(setup_teardown, print_emulation, printjob, outputsaver, tray, print_mapper):
    default = tray.get_default_source()
    tray_test_name = print_mapper.get_media_input_test_name(default)
    if tray.is_size_supported('iso_a4_210x297mm', default):
        print_emulation.tray.setup_tray(tray_test_name, MediaSize.A4.name, MediaType.Plain.name)
    printjob.print_verify('a1ebe561325c2b4764cb55cbfdde3a3ed7907bd44f16760ee34523d7861a2a1a', timeout=180)
    outputsaver.save_output()
    print_emulation.tray.reset_trays()

    logging.info("PWG A4 600x8 Color One Pagecompleted successfully")
