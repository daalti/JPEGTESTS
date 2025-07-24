import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Adding new system tests for PCL5 missing coverage
    +test_tier:1
    +is_manual:False
    +test_classification:1
    +reqid:DUNE-197464
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:jpostd.pcl=f185748f0a52dc14d07175ff17cfdc199d6ff9ea677dc434adbcb107186aa216
    +name:test_pcl5_jpostd
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_jpostd
        +guid:0d96c188-dfa7-48fc-9503-61d42de54e34
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_jpostd(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('f185748f0a52dc14d07175ff17cfdc199d6ff9ea677dc434adbcb107186aa216')
    outputsaver.save_output()