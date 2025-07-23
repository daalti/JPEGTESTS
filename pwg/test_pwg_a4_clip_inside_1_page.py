import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg a4 job with margin layout as clip inside
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:ClipInside_WSD.prn=fa41dfb8b75d165644446618818135dcdcf835d6abb595b087c8b663aae8b6af
    +name:test_pwg_a4_clip_inside_1_page
    +test:
        +title:test_pwg_a4_clip_inside_1_page
        +guid:d981e489-d60f-4643-93fd-ee567657110d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_a4_clip_inside_1_page(setup_teardown, print_emulation, printjob, outputsaver, tray, print_mapper, udw):
    outputsaver.validate_crc_tiff(udw)
    
    default = tray.get_default_source()
    tray_test_name = print_mapper.get_media_input_test_name(default)
    if tray.is_size_supported('iso_a4_210x297mm', default):
        print_emulation.tray.setup_tray(tray_test_name, MediaSize.A4.name, MediaType.Plain.name)
    printjob.print_verify('fa41dfb8b75d165644446618818135dcdcf835d6abb595b087c8b663aae8b6af', timeout=180)
    outputsaver.save_output()

    Current_crc_value = outputsaver.get_crc()
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    
    print_emulation.tray.reset_trays()

    logging.info("PWG A4 Clip Inside printed successfully")
