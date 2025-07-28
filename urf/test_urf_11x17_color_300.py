import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf 11x17_Color_300 page from *11x17_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:11x17_Color_300.urf=8d60c98d1d2191d25a4e72027efc53860520d7af3b840a2cf5feec0c0a0a52f5
    +name:test_urf_11x17_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_11x17_color_300_page
        +guid:035daf6c-f68f-46e1-b1b2-b7b87cdcf227
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
def test_urf_11x17_color_300_page(setup_teardown, printjob, outputsaver, udw,tray):
    outputsaver.validate_crc_tiff(udw)
    default = tray.get_default_source()
    if tray.is_size_supported('', default):
        tray.configure_tray(default, '', 'stationery')

    printjob.print_verify('8d60c98d1d2191d25a4e72027efc53860520d7af3b840a2cf5feec0c0a0a52f5')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()

    logging.info("URF 11x17 Color 300 page - Print job completed successfully")
