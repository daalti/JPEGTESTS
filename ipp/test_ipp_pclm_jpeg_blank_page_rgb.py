import pytest


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52177664 Ipp test for printing a PCLm file using attribute value media-size_letter
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-58957
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB__Blank_PNG_Source.pdf=3107067f9b73e78814f5944d4927435be385a21cf1d94bc5b522a719f1a135da
    +name:test_ipp_pclm_jpeg_blank_page_rgb
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pclm_jpeg_blank_page_rgb
        +guid:47557ba8-cba0-4cf4-a7ee-2a85028ae312
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_jpeg_blank_page_rgb(setup_teardown, printjob, outputverifier, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    ipp_test_attribs = {'document-format': 'application/PCLm', 'ipp-attribute-fidelity': 'true'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '3107067f9b73e78814f5944d4927435be385a21cf1d94bc5b522a719f1a135da')
    outputverifier.save_and_parse_output()
    outputsaver.operation_mode('NONE')
    Current_crc_value = outputsaver.get_crc()
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
