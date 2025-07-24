import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Adding new system tests for PCL5 missing coverage
    +test_tier:1
    +is_manual:False
    +test_classification:1
    +reqid:DUNE-197464
    +timeout:400
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:helv.prn=aab726f824d40df2a9bf1d962e8021c147bf41df4ea5d89175532379f911ee98
    +name:test_pcl5_helv_prn
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_helv_prn
        +guid:722a0d4d-16ff-455d-a0ac-c61319ea2433
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_helv_prn(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('aab726f824d40df2a9bf1d962e8021c147bf41df4ea5d89175532379f911ee98',expected_jobs=5,timeout=400)
    outputsaver.save_output()