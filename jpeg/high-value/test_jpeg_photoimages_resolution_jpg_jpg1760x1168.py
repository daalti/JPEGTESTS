import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: simple print job of jpeg file of photoimages resolution jpg jpg1760x1168
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_resolution_jpg_jpg1760x1168.JPG=bfd5bb0ee2970dbf4280705c8d15cc4c9d839d0ece7f87cb8fffe38fe0fc5c79
    +test_classification:System
    +name:test_jpeg_photoimages_resolution_jpg_jpg1760x1168
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_resolution_jpg_jpg1760x1168
        +guid:4ed7c12b-246b-42cb-9487-eb025634fade
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=custom

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_resolution_jpg_jpg1760x1168(setup_teardown, printjob, outputsaver, tray):
    outputsaver.operation_mode('TIFF')

    selected_media_source = ''
    for tray_capabilities in tray.capabilities["supportedInputs"]:
        selected_media_source = tray_capabilities['mediaSourceId']
        if tray.is_media_combination_supported(selected_media_source, "custom", "stationery"):
            if tray_capabilities['mediaWidthMinimum'] <= 233000 and tray_capabilities['mediaWidthMaximum'] >= 233000 and tray_capabilities['mediaLengthMinimum'] <= 155000 and tray_capabilities['mediaLengthMaximum'] >= 155000:
                tray.configure_tray(selected_media_source, "custom", 'stationery',width=233000, length=155000)
                logging.info(f"media source {selected_media_source} selected")
                break
            else:
                logging.info(f"media source {selected_media_source} does not support the required media size")
                selected_media_source = ''
        else:
            logging.info(f"media source {selected_media_source} not supported")
            selected_media_source = ''
    
    if selected_media_source == '':
        logging.info("No custom tray found")
        return
    
    printjob.print_verify('bfd5bb0ee2970dbf4280705c8d15cc4c9d839d0ece7f87cb8fffe38fe0fc5c79')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()

    logging.info("Jpeg photoimages resolution jpg jpg1760x1168 file")
