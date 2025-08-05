import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSource


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file using attribute value sides_one-sided.
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:broken2.jpg=746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc
    +test_classification:System
    +name:test_pdl_intent_ipp_jpg_media_size_paper_empty
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_jpg_media_size_paper_empty
        +guid:fa2115a1-56ff-4e60-b368-f6b8f3aa51a1
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaInputInstalled=MainRoll & MediaInputInstalled=Main

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_jpg_media_size_paper_empty(setup_teardown, printjob, outputsaver, tray, outputverifier, media,udw):
    tray.unload_media()
    ipp_test_attribs = {'document-format': 'image/jpeg', 'media': 'iso_a4_210x297mm'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
    jobid = printjob.start_ipp_print(ipp_test_file, '746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc')

    if tray.is_size_supported('iso_a4_210x297mm', 'main'):
        media.wait_for_alerts('allSourcesEmptyPrompt', 100)
        tray.configure_tray('main', 'iso_a4_210x297mm', 'stationery')
        tray.load_media('main')
        media.alert_action('allSourcesEmptyPrompt', 'ok')

    printjob.wait_verify_job_completion(jobid,"SUCCESS", timeout=120)
    outputsaver.save_output()
    
    # CRC check
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputsaver.operation_mode('NONE')
    
    outputverifier.save_and_parse_output()
    outputverifier.verify_media_source(Intents.printintent, MediaSource.main)
    tray.reset_trays()
