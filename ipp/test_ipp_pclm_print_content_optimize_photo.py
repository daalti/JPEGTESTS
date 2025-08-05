import pytest


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52177673 Ipp test for printing a URF file using attribute value print-content-optimize_photo
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-58957
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB__Photo.pdf=8871af83efe1b22416f963440859339286d88d07d610f8a3ad64a54834c344fc
    +name:test_ipp_pclm_print_content_optimize_photo
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pclm_print_content_optimize_photo
        +guid:1bebb7d5-5703-472b-896b-fb4d3a652741
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
def test_ipp_pclm_print_content_optimize_photo(setup_teardown, printjob, outputverifier, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    ipp_test_attribs = {'document-format': 'application/PCLm', 'print-content-optimize': 'photo'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '8871af83efe1b22416f963440859339286d88d07d610f8a3ad64a54834c344fc')
    outputverifier.save_and_parse_output()
    outputsaver.operation_mode('NONE')
    Current_crc_value = outputsaver.get_crc()
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
