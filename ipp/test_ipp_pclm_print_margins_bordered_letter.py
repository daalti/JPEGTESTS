import logging
from dunetuf.network.ipp.ipp_utils import get_ipp_margins_attribute_value


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52177643 IPP test for printing a PCLm file with Bordered-Letter
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-244314
    +timeout:300
    +asset:PDL_Print
    +delivery_team:Home
    +feature_team:RCB-ProductQA
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB__JPG_Source.pdf=7d4ca44443b3bde01436d323258048f7578b41d6f586e38c5b1ef5b95d52bc23
    +test_classification:System
    +name:test_ipp_pclm_print_margins_bordered_letter
    +test:
        +title:test_ipp_pclm_print_margins_bordered_letter
        +guid:519b9d64-6b5c-437c-9857-f49514fc7ecd
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in & MediaType=Plain & MediaInputInstalled=Tray1
    +overrides:
        +Home:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_print_margins_bordered_letter(setup_teardown, ews, net, tray, printjob, outputsaver, udw, close_ews, reset_tray):
    gpa_test_file = "/code/tests/print/pdl/ipp/attributes/gpa.test"
    media_top_margin = get_ipp_margins_attribute_value(net.ip_address, gpa_test_file, 'media-top-margin-supported')
    media_bottom_margin = get_ipp_margins_attribute_value(net.ip_address, gpa_test_file, 'media-bottom-margin-supported')
    media_edge_margin = get_ipp_margins_attribute_value(net.ip_address, gpa_test_file, 'media-left-margin-supported')
    logging.info(f"device top margin value is: {media_top_margin}, bottom margin value is: {media_bottom_margin}, edge margin value is: {media_edge_margin}")

    logging.info("Load letter size plain paper. Set media size and type from the EWS.")
    default_tray = tray.get_default_source()
    ews.media.load_paper_source_trays()
    ews.media.click_edit_default_tray_button(default_tray)
    ews.media.set_media_size("letter_8.5x11in")
    ews.media.set_media_type("plain")
    ews.media.set_tray_edit_data()
    ews.media.make_sure_apply_success()
    
    outputsaver.validate_crc_tiff(udw)

    test_file_path ='/code/tests/print/pdl/ipp/attributes/Letter.test'
    logging.info("Print pclm letter 600 H64 jpeg file")
    ipp_extra_command = f"-d topmargin={media_top_margin} -d edgemargin={media_edge_margin} -d botmargin={media_bottom_margin}"
    printjob.ipp_print(test_file_path, '7d4ca44443b3bde01436d323258048f7578b41d6f586e38c5b1ef5b95d52bc23', ipp_extra_command=ipp_extra_command)

    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()
