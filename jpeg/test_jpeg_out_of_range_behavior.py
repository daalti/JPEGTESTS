import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test jpeg out of range behavior on roll
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-155289
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A0-600-L.jpg=b9d02741fadecd94d682bb8b40ec433f5ab27ef63418cdcea21085d7b4e89d90
    +test_classification:System
    +name:test_jpeg_out_of_range_behavior_on_roll
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_out_of_range_behavior_on_roll
        +guid:e4c7ee48-908a-44c7-99c0-1a83e36d8c55
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaInputInstalled=MainRoll & MediaInputInstalled=Main

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_out_of_range_behavior_on_roll(setup_teardown, printjob, outputverifier, tray, media,outputsaver, udw):
    tray.unload_media()

    #Input document is landscape A0 size. It will be printed on roll by rotating it to portrait.
    ipp_test_attribs = {
        'document-format': 'image/jpeg',
        'media-size-name': 'iso_a0_841x1189mm',
        'media-source': 'main-roll'
    }

    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
    jobid = printjob.start_ipp_print(ipp_test_file, 'b9d02741fadecd94d682bb8b40ec433f5ab27ef63418cdcea21085d7b4e89d90')

    if tray.is_size_supported('iso_a0_841x1189mm', 'main-roll'):
        media.wait_for_alerts('mediaLoadFlow', 100)
        tray.configure_tray('main-roll', 'iso_a0_841x1189mm', 'stationery')
        tray.load_media('main-roll')
        media.alert_action('mediaLoadFlow', 'ok')

    printjob.wait_verify_job_completion(jobid, "SUCCESS", timeout=300)

    outputverifier.save_and_parse_output()
    tray.reset_trays()
    tray.unload_media()  # Will unload media from all trays
    tray.load_media()  # Will load media in all trays to default

    outputverifier.verify_media_source(Intents.printintent, MediaSource.mainroll)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.a0)
    
    # CRC check
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputsaver.operation_mode('NONE')

