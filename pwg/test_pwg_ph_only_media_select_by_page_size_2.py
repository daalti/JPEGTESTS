import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only media select by page size-2 page from *PwgPhOnly-MediaSelectByPageSize-2.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-MediaSelectByPageSize-2.pwg=41035fbf983e5c9ef50579fc123e0f691983900e49d970d2c6fd933d42f24c5e
    +name:test_pwg_ph_only_media_select_by_page_size_2_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_media_select_by_page_size_2_page
        +guid:5c2fdb7b-cc63-4dd9-aed8-57c8ebb2e6a5
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_media_select_by_page_size_2_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
     
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 110000 and media_length_maximum >= 85000 and  media_width_minimum <= 110000 and media_length_minimum <= 85000:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('41035fbf983e5c9ef50579fc123e0f691983900e49d970d2c6fd933d42f24c5e', 'FAILED')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("PWG Ph Only Media Select by Page Size-2 - Print job completed successfully")
