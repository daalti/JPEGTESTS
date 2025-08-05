import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52177654 IPP test for printing a PCLm file with Borderless-A4
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-244314
    +timeout:300
    +asset:PDL_Print
    +delivery_team:Home
    +feature_team:RCB-ProductQA
    +test_framework:TUF
    +external_files:PCLm_A4_600_cjpeg_H64_PgCnt1_RGB__JPG_Source.pdf=2b931e5448da2b6fbce96b836971a0f9008a4d24e0158f4a6c08aec3d288c189
    +test_classification:System
    +name:test_ipp_pclm_print_margins_borderless_a4
    +test:
        +title:test_ipp_pclm_print_margins_borderless_a4
        +guid:ff83c426-d708-400b-9f2d-06e96e4913b8
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & MediaSizeSupported=iso_a4_210x297mm & MediaType=Plain & BorderLessPrinting=True
    +overrides:
        +Home:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_print_margins_borderless_a4(setup_teardown, ews, printjob, outputsaver, udw, tray, close_ews, reset_tray):
    logging.info("Load A4, plain paper. Set media size and type from the EWS.")
    default_tray = tray.get_default_source()
    ews.media.load_paper_source_trays()
    ews.media.click_edit_default_tray_button(default_tray)
    ews.media.set_media_size("a4_210x297_mm")
    ews.media.set_media_type("plain")
    ews.media.set_tray_edit_data()
    ews.media.make_sure_apply_success()
    
    outputsaver.validate_crc_tiff(udw)

    test_file_path ='/code/tests/print/pdl/ipp/attributes/A4.test'
    ipp_extra_command = "-d topmargin=0 -d edgemargin=0 -d botmargin=0"
    printjob.ipp_print(test_file_path, '2b931e5448da2b6fbce96b836971a0f9008a4d24e0158f4a6c08aec3d288c189', ipp_extra_command=ipp_extra_command)

    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()
