import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: simple print job of jpeg file of photoimages_jpeg_greater3mb_dsc00452
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_JPEG_greater3mb_DSC00452.JPG=1c7dfd4eed3183b26bda9eb99ffceb52be901e7e6e2f4e12a0b62c1e753c0a1f
    +test_classification:System
    +name:test_jpeg_photoimages_jpeg_greater3mb_dsc00452
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_jpeg_greater3mb_dsc00452
        +guid:ec99f751-d683-489e-8a73-11cdfb4bca3b
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_jpeg_greater3mb_dsc00452(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 453333 and media_length_maximum >= 340000 and  media_width_minimum <= 453333  and media_length_minimum <= 340000:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('1c7dfd4eed3183b26bda9eb99ffceb52be901e7e6e2f4e12a0b62c1e753c0a1f')
    outputsaver.save_output()

    logging.info("Jpeg photoimages_JPEG_greater3mb_DSC00452 file")
