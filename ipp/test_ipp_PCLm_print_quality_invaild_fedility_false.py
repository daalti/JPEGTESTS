import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a pdf file using attribute value print_quality_normal
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-58957
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB__JPG_Source.pdf=7d4ca44443b3bde01436d323258048f7578b41d6f586e38c5b1ef5b95d52bc23
    +test_classification:System
    +name:test_ipp_PCLm_print_quality_invalid_fedility_false
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_PCLm_print_quality_invalid_fedility_false
        +guid:5e4b82fe-f9f6-4d98-a278-de12243cebb1
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_PCLm_print_quality_invalid_fedility_false(setup_teardown, printjob, outputverifier, outputsaver):
    outputsaver.operation_mode('TIFF')
    ipp_test_attribs = {'document-format': 'application/PCLm', 'print-quality': 7,'ipp-attribute-fidelity':'false'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '7d4ca44443b3bde01436d323258048f7578b41d6f586e38c5b1ef5b95d52bc23')
    outputverifier.save_and_parse_output()
    outputsaver.operation_mode('NONE')
