import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Legal Color from *Legal_Color.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Legal_Color.urf=1d5c80f76d86ac4c24e35788d9c93a744e1269aa0c0a1d354fd90c72c7c79a6d
    +name:test_urf_legal_color_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_legal_color_page
        +guid:217f053e-b944-40f0-bdab-53f83edb7767
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_legal_color_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('na_legal_8.5x14in', default):
        tray.configure_tray(default, 'na_legal_8.5x14in', 'stationery')
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 85000 and media_length_maximum >= 140000 and  media_width_minimum <= 85000 and media_length_minimum <= 140000:
        tray.configure_tray(default, 'custom', 'stationery')       

    printjob.print_verify('1d5c80f76d86ac4c24e35788d9c93a744e1269aa0c0a1d354fd90c72c7c79a6d')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Legal Color Page - Print job completed successfully")
