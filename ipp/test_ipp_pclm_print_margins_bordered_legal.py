import logging
from dunetuf.network.ipp.ipp_utils import get_ipp_margins_attribute_value


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52177646 IPP test for printing a PCLm file with Bordered-Legal
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-244314
    +timeout:300
    +asset:PDL_Print
    +delivery_team:Home
    +feature_team:RCB-ProductQA
    +test_framework:TUF
    +external_files:PCLm_legal_600_cjpeg_H64_PgCnt1_RGB__JPG_Source.pdf=8a68cbd1e070d1208a935ae4ba62b25dd10963ba5927fee2500b595a77fc04c9
    +test_classification:System
    +name:test_ipp_pclm_print_margins_bordered_legal
    +test:
        +title:test_ipp_pclm_print_margins_bordered_legal
        +guid:1859915d-80ca-4afd-86bf-7e387c666a4a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & MediaSizeSupported=na_legal_8.5x14in & MediaType=Plain & MediaInputInstalled=Tray1
    +overrides:
        +Home:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_print_margins_bordered_legal(setup_teardown, ews, net, printjob, outputsaver, udw, tray, close_ews, reset_tray):
    gpa_test_file = "/code/tests/print/pdl/ipp/attributes/gpa.test"
    media_top_margin = get_ipp_margins_attribute_value(net.ip_address, gpa_test_file, 'media-top-margin-supported')
    media_bottom_margin = get_ipp_margins_attribute_value(net.ip_address, gpa_test_file, 'media-bottom-margin-supported')
    media_edge_margin = get_ipp_margins_attribute_value(net.ip_address, gpa_test_file, 'media-left-margin-supported')
    logging.info(f"device top margin value is: {media_top_margin}, bottom margin value is: {media_bottom_margin}, edge margin value is: {media_edge_margin}")

    logging.info("Load legal size plain paper. Set media size and type from the EWS.")
    default_tray = tray.get_default_source()
    ews.media.load_paper_source_trays()
    ews.media.click_edit_default_tray_button(default_tray)
    ews.media.set_media_size("legal_8.5x14in")
    ews.media.set_media_type("plain")
    ews.media.set_tray_edit_data()
    ews.media.make_sure_apply_success()
    
    outputsaver.validate_crc_tiff(udw)

    test_file_path ='/code/tests/print/pdl/ipp/attributes/Legal.test'
    ipp_extra_command = f"-d topmargin={media_top_margin} -d edgemargin={media_edge_margin} -d botmargin={media_bottom_margin}"
    printjob.ipp_print(test_file_path, '8a68cbd1e070d1208a935ae4ba62b25dd10963ba5927fee2500b595a77fc04c9', ipp_extra_command=ipp_extra_command)

    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()
