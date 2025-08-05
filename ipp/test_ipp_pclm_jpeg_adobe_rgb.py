import pytest
import logging
from dunetuf.network.ipp.ipp_utils import execute_ipp_cmd


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52177661 Ipp test for printing a PCLm file using attribute value media-size_letter
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-58957
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_ADOBE-RGB__JPG_Source.pdf=39fe1b8bf99dcce812e8ad2dda3eceab4104f7949d65c1eccd792ad8a29bf3d3
    +name:test_ipp_pclm_jpeg_adobe_rgb
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pclm_jpeg_adobe_rgb
        +guid:8f7a26b8-3c9e-4197-b527-cb1f8dd7acb3
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP
    +overrides:
        +Home:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_jpeg_adobe_rgb(setup_teardown, printjob, outputverifier, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    ipp_test_attribs = {'document-format': 'application/PCLm', 'ipp-attribute-fidelity': 'true'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '39fe1b8bf99dcce812e8ad2dda3eceab4104f7949d65c1eccd792ad8a29bf3d3')
    outputverifier.save_and_parse_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc() 
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C30485369 BlankPage-JPEG(ADOBE-RGB) PCLm
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-244314
    +timeout:360
    +asset:PDL_Print
    +delivery_team:Home
    +feature_team:RCB-ProductQA
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_ADOBE-RGB__Blank_PNG_Source.pdf=b2c5a5fe2a7e2ab45618cd1a41f6e466e153b999ec2eaf13e2b365eea0d84142
    +test_classification:System
    +name:test_ipp_pclm_jpeg_blank_page_adobe_rgb
    +test:
        +title:test_ipp_pclm_jpeg_blank_page_adobe_rgb
        +guid:3a999204-cb87-4365-8e09-43f20d32d3ef
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP
    +overrides:
        +Home:
            +is_manual:False
            +timeout:360
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_jpeg_blank_page_adobe_rgb(setup_teardown, outputverifier, printjob, outputsaver, udw, job):
    job.bookmark_jobs()
    outputsaver.validate_crc_tiff(udw)

    print_file = printjob.get_file('b2c5a5fe2a7e2ab45618cd1a41f6e466e153b999ec2eaf13e2b365eea0d84142')
    ipp_test_file = '/code/tests/print/pdl/ipp/attributes/pclm_blank.test'

    returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, ipp_test_file , print_file)
    assert returncode == 0, f'Unexpected IPP response: {decoded_output[0]}'
    assert "[PASS]" in decoded_output[0], "Ipp print job is not complete with no issues."
    assert "[FAIL]" not in decoded_output[0], "Ipp print job is Failed with some issue."
    assert decoded_output[1] == '', "There is error output for Ipp Print."

    job.wait_for_no_active_jobs()
    new_job = job.get_newjobs()
    assert len(new_job) == 1, f"failed check job numbers"
    assert new_job[0]['completionState'] == 'success', "print job is not success"

    outputverifier.save_and_parse_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
