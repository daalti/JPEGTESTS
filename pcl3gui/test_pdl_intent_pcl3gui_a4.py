import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of an A4 PCL3GUI file on tray
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-161185
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:a4.pcl=6cf62f61dde512a2845b18ba53d96f8ade4fdb917d32080fac0285eb00ff5d8f
    +name:test_pdl_intent_pcl3gui_a4_on_tray
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_pcl3gui_a4_on_tray
        +guid:4adff052-9919-4cdd-a23e-ffde14c2c609
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI & PrintProtocols=IPP & MediaInputInstalled=MainRoll & MediaInputInstalled=Main

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_pcl3gui_a4_on_tray(setup_teardown, printjob, outputverifier, tray, media,outputsaver, udw):
    tray.unload_media()

    ipp_test_attribs = {
        'document-format': 'application/vnd.hp-PCL',
        'media-size-name': 'iso_a4_210x297mm',
        'media-source': 'main'
    }

    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
    jobid = printjob.start_ipp_print(ipp_test_file, '6cf62f61dde512a2845b18ba53d96f8ade4fdb917d32080fac0285eb00ff5d8f')

    if tray.is_size_supported('iso_a4_210x297mm', 'main'):
        media.wait_for_alerts('mediaLoadFlow', 100)
        tray.configure_tray('main', 'iso_a4_210x297mm', 'stationery')
        tray.load_media('main')
        media.alert_action('mediaLoadFlow', 'ok')

    printjob.wait_verify_job_completion(jobid,"SUCCESS", timeout=180)

    outputverifier.save_and_parse_output()
    tray.reset_trays()
    tray.unload_media() #Will unload media from all trays
    tray.load_media() #Will load media in all trays to default

    outputverifier.verify_media_source(Intents.printintent, MediaSource.main)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.a4)
    
    # CRC check
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputsaver.operation_mode('NONE')

