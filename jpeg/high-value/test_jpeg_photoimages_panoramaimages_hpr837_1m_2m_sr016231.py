import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: simple print job of jpeg file of photoimages_panoramaimages_hpr837_1m-2m_sr016231
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_panoramaimages_HPR837_1M-2M_SR016231.JPG=0f014240fbd5c018fc18aaf6ed0c8c1d0bc3adfb0a046db1a661008df3a6dccb
    +test_classification:System
    +name:test_jpeg_photoimages_panoramaimages_hpr837_1m_2m_sr016231
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_panoramaimages_hpr837_1m_2m_sr016231
        +guid:bfba0bf3-49db-4ba2-b5e3-a44a4b1b537d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_panoramaimages_hpr837_1m_2m_sr016231(setup_teardown, printjob, outputsaver, media, tray):

    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 41066  and media_length_maximum >= 91200 and  media_width_minimum <= 41066  and media_length_minimum <= 91200:
        tray.configure_tray(default, 'custom', 'stationery')
    jobid = printjob.start_print('0f014240fbd5c018fc18aaf6ed0c8c1d0bc3adfb0a046db1a661008df3a6dccb')
    
    # Handle media size mismatch alert
    try:
        media.wait_for_alerts('mediaMismatchSizeFlow', timeout=30)
        media.alert_action("mediaMismatchSizeFlow", "continue")
    except:
        logging.info("No mismatch alert, job printing")

    printjob.wait_verify_job_completion(jobid, 'SUCCESS', 120)
    logging.info('Print job completed with expected job status!')

    outputsaver.save_output()

    logging.info("Jpeg photoimages_panoramaimages_HPR837_1M-2M_SR016231 file")
