import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52178021 Simple print job of urf A5 Color 300 from *A5_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A5_Color_300.urf=7a77589c1f1d06836e8ff47c753e3e00a4805021d1fc18ece6fb20c0311ac745
    +name:test_urf_a5_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_a5_color_300_page
        +guid:2bcc0094-28ae-4328-85d5-584c4052db4a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=iso_a5_148x210mm
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_a5_color_300_page(setup_teardown, printjob, outputsaver, tray, udw, reset_tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a5_148x210mm', default):
        tray.configure_tray(default, 'iso_a5_148x210mm', 'stationery')
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('7a77589c1f1d06836e8ff47c753e3e00a4805021d1fc18ece6fb20c0311ac745')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc() 
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()

    logging.info("URF A5 Color 300 page - Print job completed successfully")
