import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf 12x18_Color_300 page from *12x18_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:12x18_Color_300.urf=ff4c9a88c9a971c15c60cf8a6c1c7af41ac6c9c5feeeb9f578ea925e21ea9d6d
    +name:test_urf_12x18_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_12x18_color_300_page
        +guid:d31c630f-51a0-4d73-9a88-59790243622f
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
def test_urf_12x18_color_300_page(setup_teardown, printjob, outputsaver, udw,tray):
    outputsaver.validate_crc_tiff(udw)

    default = tray.get_default_source()
    if tray.is_size_supported('na_arch-b_12x18in', default):
        tray.configure_tray(default, 'na_arch-b_12x18in', 'stationery')

    printjob.print_verify('ff4c9a88c9a971c15c60cf8a6c1c7af41ac6c9c5feeeb9f578ea925e21ea9d6d')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()

    logging.info("URF 12x18 Color 300 page - Print job completed successfully")
