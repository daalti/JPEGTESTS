import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSource


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file when all sources are empty.
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-168730
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A3_margin_portrait.jpg=d6b956d1775efee42d23dafa8ff0309a12614c6d4f0e7cea35a485057e63ab76
    +test_classification:System
    +name:test_ipp_jpg_media_size_allSourcesEmpty
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_jpg_media_size_allSourcesEmpty
        +guid:8e213189-771b-42c0-81c3-97ed68b477d8
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaInputInstalled=MainRoll & MediaInputInstalled=Main
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_jpg_media_size_allSourcesEmpty(setup_teardown, printjob, outputsaver, tray, outputverifier, media, udw):
    tray.unload_media()
    
    ipp_test_attribs = {
        'document-format': 'image/jpeg',
        'print-scaling': 'fit',
        'media-size-name': 'iso_a3_297x420mm',
        'media-bottom-margin': 499, 
        'media-left-margin': 499, 
        'media-right-margin': 499, 
        'media-top-margin': 499, 
        'print-quality': 3        
    }

    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
    jobid = printjob.start_ipp_print(ipp_test_file, 'd6b956d1775efee42d23dafa8ff0309a12614c6d4f0e7cea35a485057e63ab76')

    if tray.is_size_supported('iso_a3_297x420mm', 'main'):
        media.wait_for_alerts('allSourcesEmptyPrompt', 100)
        tray.configure_tray('main', 'iso_a3_297x420mm', 'stationery')
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
    tray.load_media('main-roll')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file when all sources are empty. Job MediaSource is Roll
    +test_tier: 1
    +is_manual: False
    +reqid: DUNE-168730
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files: A3_margin_portrait.jpg=d6b956d1775efee42d23dafa8ff0309a12614c6d4f0e7cea35a485057e63ab76
    +test_classification:System
    +name: test_ipp_jpg_media_size_allSourcesEmpty_MediaSourceReqIsRoll
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_ipp_jpg_media_size_allSourcesEmpty_MediaSourceReqIsRoll
        +guid:511a6d78-861d-4ef0-818d-e8ee86221e52
        +dut:
            +type: Simulator
            +configuration: DocumentFormat=JPEG & PrintProtocols=IPP & MediaInputInstalled=MainRoll & MediaInputInstalled=Main
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_jpg_media_size_allSourcesEmpty_MediaSourceReqIsRoll(setup_teardown, printjob, outputsaver, tray, outputverifier, media, udw):
    tray.unload_media()

    ipp_test_attribs = {
        'document-format': 'image/jpeg',
        'print-scaling': 'fit',
        'media-size-name': 'iso_a3_297x420mm',
        'media-source': 'main-roll',
        'media-bottom-margin': 499, 
        'media-left-margin': 499, 
        'media-right-margin': 499, 
        'media-top-margin': 499, 
        'print-quality': 3        
    }

    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
    jobid = printjob.start_ipp_print(ipp_test_file, 'd6b956d1775efee42d23dafa8ff0309a12614c6d4f0e7cea35a485057e63ab76')

    if tray.is_size_supported('iso_a3_297x420mm', 'main-roll'):
        media.wait_for_alerts('mediaLoadFlow', 100)
        tray.configure_tray('main-roll', 'iso_a3_297x420mm', 'stationery')
        tray.load_media('main-roll')
        media.alert_action('mediaLoadFlow', 'ok')

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
    outputverifier.verify_media_source(Intents.printintent, MediaSource.mainroll)
    tray.reset_trays()
    tray.load_media('main-roll')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file when all sources are empty. Job MediaSource is Main Tray
    +test_tier: 1
    +is_manual: False
    +reqid: DUNE-168730
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files: A3_margin_portrait.jpg=d6b956d1775efee42d23dafa8ff0309a12614c6d4f0e7cea35a485057e63ab76
    +test_classification:System
    +name: test_ipp_jpg_media_size_allSourcesEmpty_MediaSourceReqIsMainTray
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_ipp_jpg_media_size_allSourcesEmpty_MediaSourceReqIsMainTray
        +guid:cd66335b-a3cb-4e90-b4b8-9b9f95eb38b3
        +dut:
            +type: Simulator
            +configuration: DocumentFormat=JPEG & PrintProtocols=IPP & MediaInputInstalled=MainRoll & MediaInputInstalled=Main
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_ipp_jpg_media_size_allSourcesEmpty_MediaSourceReqIsMainTray(setup_teardown, printjob, outputsaver, tray, outputverifier, media, udw):
    tray.unload_media()
    
    ipp_test_attribs = {
        'document-format': 'image/jpeg',
        'print-scaling': 'fit',
        'media-size-name': 'iso_a3_297x420mm',
        'media-source': 'main',
        'media-bottom-margin': 499, 
        'media-left-margin': 499, 
        'media-right-margin': 499, 
        'media-top-margin': 499, 
        'print-quality': 3        
    }

    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
    jobid = printjob.start_ipp_print(ipp_test_file, 'd6b956d1775efee42d23dafa8ff0309a12614c6d4f0e7cea35a485057e63ab76')

    if tray.is_size_supported('iso_a3_297x420mm', 'main'):
        media.wait_for_alerts('mediaLoadFlow', 100)
        tray.configure_tray('main', 'iso_a3_297x420mm', 'stationery')
        tray.load_media('main')
        media.alert_action('mediaLoadFlow', 'ok')

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
    tray.load_media('main-roll')

