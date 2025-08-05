import pytest

from dunetuf.print.output.intents import Intents


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a PCLm file **
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-58957
    +timeout:360
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB__JPG_Source.pdf=7d4ca44443b3bde01436d323258048f7578b41d6f586e38c5b1ef5b95d52bc23
    +test_classification:System
    +name:test_ipp_pclm_copies_2_fedility_true
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pclm_copies_2_fedility_true
        +guid:60d30420-ec12-43a0-bfed-565a76275be0
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & Print=NumberOfCopies

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_copies_2_fedility_true (setup_teardown, printjob, outputverifier, outputsaver,udw):
    outputsaver.operation_mode('TIFF')
    REQUIRED_MEMORY = 52428800
    if printjob.printer_has_enough_pdl_memory(udw, REQUIRED_MEMORY):
        ipp_test_attribs = {'document-format': 'application/PCLm', 'copies': 2, 'ipp-attribute-fidelity': 'true'}
    else:
         ipp_test_attribs = {'document-format': 'application/PCLm', 'copies': 1, 'ipp-attribute-fidelity': 'true'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '7d4ca44443b3bde01436d323258048f7578b41d6f586e38c5b1ef5b95d52bc23')
    outputverifier.save_and_parse_output()
    outputsaver.operation_mode('NONE')
