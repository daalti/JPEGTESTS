import pytest
import logging

from dunetuf.print.output.intents import Intents
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
    +name:test_ipp_pclm_validate_get_job_attribute
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pclm_validate_get_job_attribute
        +guid:d9a26373-466b-4856-9246-1946c8be9b46
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_validate_get_job_attribute(setup_teardown, printjob, outputverifier):
    job_attribute = ['time-at-creation', 'time-at-processing', 'time-at-completed']
    flag = []
    print_file = printjob.get_file('7d4ca44443b3bde01436d323258048f7578b41d6f586e38c5b1ef5b95d52bc23')

    printjob.bookmark_jobs()
    returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, '/code/tests/print/pdl/ipp/get_job_attributes/get-job-attributes.test', print_file)
    print(f"decoded_ouput type {type(decoded_output)}")
    decoded_output = decoded_output[0].split("\n")
    for jobattr in range(len(job_attribute)):
       s = job_attribute[jobattr]
       for line in decoded_output:
         if s in line:
          flag.append(line)             

       for job_attr in range(len(job_attribute)):
        f=job_attribute[job_attr]
        for f in flag:
          if f not in flag:
            assert False, f"Job attribute {job_attribute[job_attr]} not found"
          else:
              logging.info(f"Job attribute {job_attribute[job_attr]} found")

    outputverifier.save_and_parse_output()

