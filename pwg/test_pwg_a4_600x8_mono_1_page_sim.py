import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg a4 600x8 mono one page from *a4-600x8-mono-1p-sim.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:a4-600x8-mono-1p-sim.pwg=706dc4ec7cc7102294bd874d627301bbbb8e84c18378528ffd59ba63639f1697
    +name:test_pwg_a4_600x8_mono_one_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_a4_600x8_mono_one_page
        +guid:4695b8aa-0bf3-405e-b1ec-63fe008c93a6
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster
    +overrides:
        +Home:
            +is_manual:False
            +timeout:360
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_a4_600x8_mono_one_page(setup_teardown, print_emulation, printjob, outputsaver, tray, print_mapper):
    default = tray.get_default_source()
    tray_test_name = print_mapper.get_media_input_test_name(default)
    if tray.is_size_supported('iso_a4_210x297mm', default):
        print_emulation.tray.setup_tray(tray_test_name, MediaSize.A4.name, MediaType.Plain.name)

    printjob.print_verify('706dc4ec7cc7102294bd874d627301bbbb8e84c18378528ffd59ba63639f1697')
    outputsaver.save_output()
    print_emulation.tray.reset_trays()

    logging.info("PWG A4 600x8 Mono One Pagecompleted successfully")