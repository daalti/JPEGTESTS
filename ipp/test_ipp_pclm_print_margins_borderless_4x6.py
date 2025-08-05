import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52177655 IPP test for printing a PCLm file with Borderless-4x6 in
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-244314
    +timeout:300
    +asset:PDL_Print
    +delivery_team:Home
    +feature_team:RCB-ProductQA
    +test_framework:TUF
    +external_files:PCLm_4x6_600_cjpeg_H64_PgCnt1_RGB__JPG_Source.pdf=7fe66016415859546a91e2a9aef6577b27e33f5960710f30378330dfa0852b72
    +test_classification:System
    +name:test_ipp_pclm_print_margins_borderless_4x6
    +test:
        +title:test_ipp_pclm_print_margins_borderless_4x6
        +guid:151f0ee5-97c3-41c8-ae76-f47193853847
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & MediaSizeSupported=na_index-4x6_4x6in & MediaType=HPAdvancedPhotoPapers & BorderLessPrinting=True
    +overrides:
        +Home:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_print_margins_borderless_4x6(setup_teardown, ews, printjob, outputsaver, tray, udw, close_ews, reset_tray):
    logging.info("Load 4x6 photo glossy paper. Set media size and type from the EWS.")
    default_tray = tray.get_default_source()
    ews.media.load_paper_source_trays()
    ews.media.click_edit_default_tray_button(default_tray)
    ews.media.set_media_size("4x6in")
    ews.media.set_media_type("hp_advanced_photo")
    ews.media.set_tray_edit_data()
    ews.media.make_sure_apply_success()
    
    outputsaver.validate_crc_tiff(udw)

    test_file_path ='/code/tests/print/pdl/ipp/attributes/4x6_Photo.test'
    ipp_extra_command = "-d topmargin=0 -d edgemargin=0 -d botmargin=0"
    printjob.ipp_print(test_file_path, '7fe66016415859546a91e2a9aef6577b27e33f5960710f30378330dfa0852b72', ipp_extra_command=ipp_extra_command)

    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()
