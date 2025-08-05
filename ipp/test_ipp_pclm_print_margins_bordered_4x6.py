import logging
from dunetuf.network.ipp.ipp_utils import get_ipp_margins_attribute_value


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52177644 IPP test for printing a PCLm file with Bordered-4x6 in
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
    +name:test_ipp_pclm_print_margins_bordered_4x6
    +test:
        +title:test_ipp_pclm_print_margins_bordered_4x6
        +guid:6e45bccf-656b-4ddf-83cf-ee6797bea01c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & MediaSizeSupported=na_index-4x6_4x6in & MediaType=HPAdvancedPhotoPapers
    +overrides:
        +Home:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_print_margins_bordered_4x6(setup_teardown, ews, net, printjob, outputsaver, tray, udw, close_ews, reset_tray):
    gpa_test_file = "/code/tests/print/pdl/ipp/attributes/gpa.test"
    media_top_margin = get_ipp_margins_attribute_value(net.ip_address, gpa_test_file, 'media-top-margin-supported')
    media_bottom_margin = get_ipp_margins_attribute_value(net.ip_address, gpa_test_file, 'media-bottom-margin-supported')
    media_edge_margin = get_ipp_margins_attribute_value(net.ip_address, gpa_test_file, 'media-left-margin-supported')
    logging.info(f"device top margin value is: {media_top_margin}, bottom margin value is: {media_bottom_margin}, edge margin value is: {media_edge_margin}")

    logging.info("Load 4x6 photo glossy paper. Set media size and type from the EWS.")
    default_tray = tray.get_default_source()
    ews.media.load_paper_source_trays()
    ews.media.click_edit_default_tray_button(default_tray)
    ews.media.set_media_size("4x6in")
    ews.media.set_media_type("hp_advanced_photo")
    ews.media.set_tray_edit_data()
    ews.media.make_sure_apply_success()
    
    outputsaver.validate_crc_tiff(udw)

    test_file_path = '/code/tests/print/pdl/ipp/attributes/4x6_Photo.test'
    ipp_extra_command = f"-d topmargin={media_top_margin} -d edgemargin={media_edge_margin} -d botmargin={media_bottom_margin}"
    printjob.ipp_print(test_file_path, '7fe66016415859546a91e2a9aef6577b27e33f5960710f30378330dfa0852b72', ipp_extra_command=ipp_extra_command)

    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()
