import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf 10x12 custom job on roll
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-128384
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:10x12_URF.urf=68ad2334e87b103fda5d9502f4a5d34417cc349b8ef0fb182b56385441faa639
    +name:test_urf_custom_job_10x12_on_roll
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_custom_job_10x12_on_roll
        +guid:069e3dd4-68da-45e9-b722-7e062a63e27a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & PrintProtocols=IPP & MediaInputInstalled=MainRoll & MediaInputInstalled=Main

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_custom_job_10x12_on_roll(setup_teardown, printjob, outputverifier, tray, media,outputsaver, udw):
    tray.unload_media()

    ipp_test_attribs = {
        'document-format': 'image/urf',
        'media-source': 'auto',
        'x-dimension': '25400',
        'y-dimension': '30480',
        'media-bottom-margin': 499,
        'media-left-margin': 499,
        'media-right-margin': 499,
        'media-top-margin': 499,
    }

    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
    jobid = printjob.start_ipp_print(ipp_test_file, '68ad2334e87b103fda5d9502f4a5d34417cc349b8ef0fb182b56385441faa639')

    if tray.is_size_supported('iso_a0_841x1189mm', 'main-roll'):
        media.wait_for_alerts('allSourcesEmptyPrompt', 100)
        tray.configure_tray('main-roll', 'iso_a0_841x1189mm', 'stationery')
        tray.load_media('main-roll')
        media.alert_action('allSourcesEmptyPrompt', 'ok')

    printjob.wait_verify_job_completion(jobid,"SUCCESS", timeout=300)

    outputverifier.save_and_parse_output()
    tray.reset_trays()
    tray.unload_media() #Will unload media from all trays
    tray.load_media() #Will load media in all trays to default

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

