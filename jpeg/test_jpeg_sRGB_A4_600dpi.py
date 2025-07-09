import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of jpeg_sRGB_A4_600dpi
    +test_tier:1
    +is_manual:True
    +reqid:DUNE-18107
    +timeout:300
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:sRGB_A4_600dpi.jpg=86c81bfee5d3a323f7faf4026db8bf534e9d8edf624b9170bb60e3cf2d59773b
    +test_classification:System
    +name:test_jpeg_sRGB_A4_600dpi
    +test:
        +title:test_jpeg_sRGB_A4_600dpi
        +guid:960f2274-0fb3-11eb-8419-c7d8ee3a6970
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_sRGB_A4_600dpi(setup_teardown, printjob, outputsaver, tray):
    outputsaver.operation_mode('TIFF')

    default = tray.get_default_source()
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    else:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('86c81bfee5d3a323f7faf4026db8bf534e9d8edf624b9170bb60e3cf2d59773b', timeout=300)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()

    logging.info("Jpeg sRGB_A4_600dpi- Print job completed successfully")
