import pytest
import logging
from dunetuf.network.ipp.ipp_utils import execute_ipp_cmd


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a URF file using attribute value print-content-optimize_text_and_graphics
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-58957
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB__Graphics.pdf=5d2c2739f4126a4a74d3a9da7d3d261255f572999dd4abd3957f734561c0c240
    +name:test_ipp_pclm_print_content_optimize_text_and_graphics
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pclm_print_content_optimize_text_and_graphics
        +guid:031a3883-0fcd-40ef-9049-e2407786699f
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_print_content_optimize_text_and_graphics(setup_teardown, printjob, outputverifier, outputsaver):
    outputsaver.operation_mode('TIFF')
    ipp_test_attribs = {'document-format': 'image/urf', 'print-content-optimize': 'text-and-graphics'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '5d2c2739f4126a4a74d3a9da7d3d261255f572999dd4abd3957f734561c0c240')
    outputverifier.save_and_parse_output()
    outputsaver.operation_mode('NONE')



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C30485386 Print_Content_Optimize-optimize-text-and-graphics
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-244314
    +timeout:360
    +asset:PDL_Print
    +delivery_team:Home
    +feature_team:RCB-ProductQA
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB__TextGraphicsColor.pdf=8a10be5fa5db739b4454c82329533a2e030d79d1bd285fff0620e3aadc32980b
    +test_classification:System
    +name:test_ipp_pclm_print_pclm_letter_600_cjpeg_h64_pgcnt1_rgb_text_graphics_color
    +test:
        +title:test_ipp_pclm_print_pclm_letter_600_cjpeg_h64_pgcnt1_rgb_text_graphics_color
        +guid:909b1bc0-565f-4d99-a812-6d7a68a671b0
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCLm & PrintProtocols=IPP
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_print_pclm_letter_600_cjpeg_h64_pgcnt1_rgb_text_graphics_color(setup_teardown, printjob, outputverifier, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)

    print_file = printjob.get_file('8a10be5fa5db739b4454c82329533a2e030d79d1bd285fff0620e3aadc32980b')
    ipp_test_file = "/code/tests/print/pdl/ipp/attributes/print-content-optimize-text-and-graphics.test"
    
    returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, ipp_test_file , print_file)
    assert returncode == 0, f'Unexpected IPP response: {decoded_output[0]}'
    assert "[PASS]" in decoded_output[0], "Ipp print job is not complete with no issues."
    assert "[FAIL]" not in decoded_output[0], "Ipp print job is Failed with some issue."
    assert "print-content-optimize (keyword) = text-and-graphics" in decoded_output[0], "Text and Graphics should not be seen for the listed attribute."
    assert decoded_output[1] == '', "There is error output for Ipp Print."

    outputverifier.save_and_parse_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
