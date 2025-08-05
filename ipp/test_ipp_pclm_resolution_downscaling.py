import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a 600 dpi PCLm file at 300 dpi.
    +test_tier:1
    +is_manual:False
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +reqid:DUNE-206291
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB__JPG_Source.pdf=7d4ca44443b3bde01436d323258048f7578b41d6f586e38c5b1ef5b95d52bc23
    +test_classification:System
    +name:test_ipp_pclm_resolution_downscaling
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pclm_resolution_downscaling
        +guid:bb861e26-d255-4775-8477-24926a4b4ce5
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP  & PrintResolution=Print300

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_resolution_downscaling(setup_teardown, printjob, outputsaver, tray,cdm,configuration):    

    ipp_test_attribs = {'document-format': 'application/PCLm', 'resolution': '300x300dpi'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '7d4ca44443b3bde01436d323258048f7578b41d6f586e38c5b1ef5b95d52bc23',timeout=600)
    outputsaver.save_output()