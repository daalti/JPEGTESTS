import logging
from dunetuf.network.ipp.ipp_utils import execute_ipp_cmd, get_ipp_margins_attribute_value


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C30485334 Margins-ZLIB - Validate that the DUT handles marginned PCLm documents
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-244314
    +timeout:300
    +asset:PDL_Print
    +delivery_team:Home
    +feature_team:RCB-ProductQA
    +test_framework:TUF
    +external_files:PCLm_letter_600_czlib_H32_PgCnt1_RGB__JPG_Source.pdf=f64abd0480441505d7d406346ac765c856c0f305ac6a938b8c1322f5c7384176
    +external_files:PCLm_letter_600_czlib_H64_PgCnt1_RGB__JPG_Source.pdf=dc1875400c330b682b34a204def7e01dde4f1f94439c2261e795c1ccef88e8ef
    +test_classification:System
    +name:test_ipp_pclm_print_margins_zlib_marginned_pclm_documents
    +test:
        +title:test_ipp_pclm_print_margins_zlib_marginned_pclm_documents
        +guid:d05ab0c2-f0fd-4c13-9124-8598e29dc102
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in
    +overrides:
        +Home:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_print_margins_zlib_marginned_pclm_documents(setup_teardown, net, tray, printjob, outputsaver, udw, job, reset_tray):
    job.bookmark_jobs()
    gpa_test_file = "/code/tests/print/pdl/ipp/attributes/gpa.test"
    media_top_margin = get_ipp_margins_attribute_value(net.ip_address, gpa_test_file, 'media-top-margin-supported')
    media_bottom_margin = get_ipp_margins_attribute_value(net.ip_address, gpa_test_file, 'media-bottom-margin-supported')
    media_edge_margin = get_ipp_margins_attribute_value(net.ip_address, gpa_test_file, 'media-left-margin-supported')
    logging.info(f"device top margin value is: {media_top_margin}, bottom margin value is: {media_bottom_margin}, edge margin value is: {media_edge_margin}")

    default = tray.get_default_source()
    if tray.is_size_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')
    
    outputsaver.validate_crc_tiff(udw)

    test_file_path='/code/tests/print/pdl/ipp/attributes/Letter.test'  

    logging.info("Print pclm letter 600 H32 zlib file")
    print_file = printjob.get_file('f64abd0480441505d7d406346ac765c856c0f305ac6a938b8c1322f5c7384176')
    ipp_extra_command = f"-d topmargin={media_top_margin} -d edgemargin={media_edge_margin} -d botmargin={media_bottom_margin}"
    returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, test_file_path, print_file, ipp_extra_command=ipp_extra_command)
    logging.info(f"Ipp print output content is: <{decoded_output}>")
    assert returncode == 0, f'Unexpected IPP response: {returncode}'
    assert "[PASS]" in decoded_output[0], "Ipp print job is not complete with no issues."
    assert "[FAILED]" not in decoded_output[0], "check Ipptool reports all subtests [PASS] is failed"
    assert decoded_output[1] == '', "There is error output for Ipp Print."
    job.wait_for_no_active_jobs()
    new_job = job.get_newjobs()
    assert len(new_job) == 1, f"failed to check job lens, new job info: {new_job}"
    assert new_job[-1].get('completionState') == 'success', 'Print job is not success'
    job.bookmark_jobs()
    
    logging.info("Print pclm letter 600 H64 zlib file")
    print_file = printjob.get_file('dc1875400c330b682b34a204def7e01dde4f1f94439c2261e795c1ccef88e8ef')
    returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, test_file_path, print_file, ipp_extra_command=ipp_extra_command)
    logging.info(f"Ipp print output content is: <{decoded_output}>")
    assert returncode == 0, f'Unexpected IPP response: {returncode}'
    assert "[PASS]" in decoded_output[0], "Ipp print job is not complete with no issues."
    assert "[FAILED]" not in decoded_output[0], "check Ipptool reports all subtests [PASS] is failed"
    assert decoded_output[1] == '', "There is error output for Ipp Print."
    job.wait_for_no_active_jobs()
    new_job = job.get_newjobs()
    assert len(new_job) == 1, f"failed to check job lens, new job info: {new_job}"
    assert new_job[-1].get('completionState') == 'success', 'Print job is not success'

    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"  
    tray.reset_trays()
