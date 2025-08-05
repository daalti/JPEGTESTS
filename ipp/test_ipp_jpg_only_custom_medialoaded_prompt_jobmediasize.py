import pytest
import logging

from dunetuf.print.output.intents import Intents, MediaSize, MediaSource

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file when only custom media size is loaded.
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-259441
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:broken2.jpg=746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc
    +test_classification:System
    +name:test_ipp_jpg_only_custom_medialoaded_prompt_jobmediasize
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_jpg_only_custom_medialoaded_prompt_jobmediasize
        +guid:42435b11-b2ab-4346-a6af-cb0f2e62a877
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaSizeSupported=custom & MediaSizeSupported=iso_a4_210x297mm & MediaInputInstalled=Tray1

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_jpg_only_custom_medialoaded_prompt_jobmediasize(setup_teardown, printjob, udw, outputsaver, tray, media, outputverifier):

    ipp_test_attribs = {'document-format': 'image/jpeg', 'media': 'iso_a4_210x297mm'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    # configure the tray to have custom media size
    tray.unload_media()
    tray.configure_all_trays(media_size='custom', media_type='stationery', width=70000, length=70000, resolution=10000)
    jobid = printjob.start_ipp_print(ipp_test_file, '746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc')

    # Handle media size mismatch alert
    try:
        media.wait_for_alerts('mediaMismatchSizeFlow', timeout=30)
        tray.configure_tray('tray-1', 'iso_a4_210x297mm', 'stationery')
        tray.load_media('tray-1')
        media.alert_action('mediaMismatchSizeFlow', 'ok')
    except:
        logging.info("No mismatch alert, job printing")

    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.a4)