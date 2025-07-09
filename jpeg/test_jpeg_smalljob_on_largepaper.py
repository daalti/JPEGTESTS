import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test jpeg small job on large paper tray
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-153638
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:abbey-4x6-L.jpg=1fcc44e51d4702a75c0487be852ae62fca82a2cab4bf0d19645b83e3264eb1d0
    +test_classification:System
    +name:test_jpeg_smalljob_on_largepaper_on_tray
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_smalljob_on_largepaper_on_tray
        +guid:cbbe32f9-bad7-4671-866e-a68b3b3fdc67
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaInputInstalled=MainRoll & MediaInputInstalled=Main

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_smalljob_on_largepaper_on_tray(setup_teardown, printjob, outputverifier, tray, media,outputsaver, udw):
    tray.unload_media()
    if tray.is_size_supported('iso_a4_210x297mm', 'main'):
        tray.configure_tray('main', 'iso_a4_210x297mm', 'stationery')
        tray.load_media('main')
    
    ipp_test_attribs = {
        'document-format': 'image/jpeg',
        'media-source': 'main'
    }

    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
    jobid = printjob.start_ipp_print(ipp_test_file, '1fcc44e51d4702a75c0487be852ae62fca82a2cab4bf0d19645b83e3264eb1d0')

    printjob.wait_verify_job_completion(jobid, "SUCCESS", timeout=180)

    outputverifier.save_and_parse_output()
    tray.reset_trays()
    tray.unload_media()  # Will unload media from all trays
    tray.load_media()  # Will load media in all trays to default

    outputverifier.verify_media_source(Intents.printintent, MediaSource.main)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.a4)  # coming as a4 due to jpeg scaling
    
    # CRC check
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputsaver.operation_mode('NONE')

