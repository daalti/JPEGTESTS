import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52178020 Simple print job of urf A3 Color 600 from *A3_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:300
    +asset:PDL_Print
    +delivery_team:LFP 
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:A3_Color_600.urf=974aee85965b8d8cb63584d8661e1d87c0d57893c6447dc010a49e4b9961a7dd
    +name:test_urf_a3_color_600_page
    +test:
        +title:test_urf_a3_color_600_page
        +guid:389e920f-438f-4ef5-a95b-b9a89a6509ec
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_a3_color_600_page(setup_teardown, printjob, outputsaver, tray, udw, reset_tray):
    outputsaver.operation_mode('TIFF')

    default = tray.get_default_source()
    if tray.is_size_supported('iso_a3_297x420mm', default):
        tray.configure_tray(default, 'iso_a3_297x420mm', 'stationery')
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('974aee85965b8d8cb63584d8661e1d87c0d57893c6447dc010a49e4b9961a7dd', timeout=300)
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc() 
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputsaver.operation_mode('NONE')
    tray.reset_trays()

    logging.info("URF A3 Color 600 page - Print job completed successfully")
