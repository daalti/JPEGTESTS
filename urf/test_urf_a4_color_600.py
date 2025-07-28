import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType, MediaOrientation

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf A4 Color 600 from *A4_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A4_Color_600.urf=2dbe67f5a803639fd902f1a097d90b287de362650cd198829801c9f477337ff0
    +name:test_urf_a4_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_a4_color_600_page
        +guid:5cac7ce6-5329-477a-8099-584656db3f31
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_a4_color_600_page(setup_teardown, printjob, print_emulation, configuration, outputsaver,udw,tray):
    outputsaver.validate_crc_tiff(udw)
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        if print_emulation.print_engine_platform == 'emulator' and configuration.familyname == 'enterprise':
            tray1 = MediaInputIds.Tray1.name
            print_emulation.tray.open(tray1)
            print_emulation.tray.load(tray1, MediaSize.A4.name, MediaType.Plain.name)
            print_emulation.tray.close(tray1)
        else:
            tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

    printjob.print_verify('2dbe67f5a803639fd902f1a097d90b287de362650cd198829801c9f477337ff0')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()

    logging.info("URF A4 Color 600 page - Print job completed successfully")
