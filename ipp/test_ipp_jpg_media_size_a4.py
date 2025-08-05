import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C51669540 IPP test for printing a JPG file using attribute value media_size_A4
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-244314
    +timeout:180
    +asset:PDL_Print
    +delivery_team:Home
    +feature_team:RCB-ProductQA
    +test_framework:TUF
    +external_files:sRGB_A4_600dpi.jpg=86c81bfee5d3a323f7faf4026db8bf534e9d8edf624b9170bb60e3cf2d59773b
    +test_classification:System    
    +name:test_ipp_jpg_media_size_a4
    +test:
        +title:test_ipp_jpg_media_size_a4
        +guid:e2ecbc2a-1230-4a54-91ce-1c32e9071f5e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=A4 & PrintProtocols=IPP
    +overrides:
        +Home:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_jpg_media_size_a4(setup_teardown, reset_tray, printjob, outputsaver, tray, udw):
    outputsaver.validate_crc_tiff(udw)
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

    ipp_test_attribs = {'document-format': 'image/jpeg', 'media-size-name': 'iso_a4_210x297mm'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '86c81bfee5d3a323f7faf4026db8bf534e9d8edf624b9170bb60e3cf2d59773b')

    outputsaver.save_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info(f"Validate current crc <{Current_crc_value}> with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
