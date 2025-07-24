import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Adding new system tests for PCL5 missing coverage
    +test_tier:1
    +is_manual:False
    +test_classification:1
    +reqid:DUNE-197464
    +timeout:500
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:MediaDest0-5.pcl=0e794dccb160967c819cd4a48c35c9f916dad145ef3af8a0ef7816cfe60e5b58
    +name:test_pcl5_mediadest0_5
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_mediadest0_5
        +guid:84f63fe0-36a0-4cf1-be26-d1c110a79862
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_mediadest0_5(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('0e794dccb160967c819cd4a48c35c9f916dad145ef3af8a0ef7816cfe60e5b58',expected_jobs=6,timeout=500)
    outputsaver.save_output()