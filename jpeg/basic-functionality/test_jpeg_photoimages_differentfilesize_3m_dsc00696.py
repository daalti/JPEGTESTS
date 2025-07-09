import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:simple print job of jpeg file of photoimages differentfilesize 3m dsc00696
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_differentfilesize_3M_DSC00696.JPG=9ba3d34b6493769d9d1b40252c3ed9e360de6f4e3e0c93029f616516698637c4
    +test_classification:System
    +name:test_jpeg_photoimages_differentfilesize_3m_dsc00696
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_differentfilesize_3m_dsc00696
        +guid:21edabdb-3181-4f01-8792-0fe468c7fac9
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_differentfilesize_3m_dsc00696(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 453333 and media_length_maximum >= 340000 and  media_width_minimum <= 453333 and media_length_minimum <= 340000:
        tray.configure_tray(default, 'custom', 'stationery')


    printjob.print_verify('9ba3d34b6493769d9d1b40252c3ed9e360de6f4e3e0c93029f616516698637c4')
    outputsaver.save_output()

    logging.info("Jpeg file example photoimages differentfilesize 3M DSC00696 - Print job completed successfully")
