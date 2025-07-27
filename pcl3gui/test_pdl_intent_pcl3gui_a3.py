import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of an A3 PCL3GUI file on tray
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-169798
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:a3.pcl=73673f25fd8f3526728f3cef33d394411e28372bd5706f41687a407d6cf341ad
    +name:test_pdl_intent_pcl3gui_a3_on_tray
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_pcl3gui_a3_on_tray
        +guid:341e65f6-0af3-4914-ac58-84b4c6076d43
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI & PrintProtocols=IPP & MediaInputInstalled=MainRoll & MediaInputInstalled=Main

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_pcl3gui_a3_on_tray(setup_teardown, printjob, outputverifier, tray, media):
    tray.unload_media()

    ipp_test_attribs = {
        'document-format': 'application/vnd.hp-PCL',
        'media-size-name': 'iso_a3_297x420mm',
        'media-source': 'main'
    }

    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
    jobid = printjob.start_ipp_print(ipp_test_file, '73673f25fd8f3526728f3cef33d394411e28372bd5706f41687a407d6cf341ad')

    if tray.is_size_supported('iso_a3_297x420mm', 'main'):
        media.wait_for_alerts('mediaLoadFlow', 100)
        tray.configure_tray('main', 'iso_a3_297x420mm', 'stationery')
        tray.load_media('main')
        media.alert_action('mediaLoadFlow', 'ok')

    printjob.wait_verify_job_completion(jobid,"SUCCESS", timeout=180)

    outputverifier.save_and_parse_output()
    tray.reset_trays()
    tray.unload_media() #Will unload media from all trays
    tray.load_media() #Will load media in all trays to default

    outputverifier.verify_media_source(Intents.printintent, MediaSource.main)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.a3)

