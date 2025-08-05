import pytest

from dunetuf.network.ipp.ipp_utils import execute_ipp_cmd


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
    +name:test_ipp_pclm_validate_print_job
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pclm_validate_print_job
        +guid:c05047c0-e8af-4806-8c87-75d062764ae3
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_validate_print_job(setup_teardown, printjob, outputverifier, outputsaver):
    outputsaver.operation_mode('TIFF')
    print_file = printjob.get_file('7d4ca44443b3bde01436d323258048f7578b41d6f586e38c5b1ef5b95d52bc23')
    returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, '/code/output/time-at.test', print_file)
    outputverifier.save_and_parse_output()
    outputsaver.operation_mode('NONE')
