import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using 3pg_2mopy.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:3pg_2mopy.pcl=7fc0f1f953fb570ee1cb9074f341c91674d8d82445777e74cd463bdc5a93c65d
    +test_classification:System
    +name: test_pcl5_testfiles_masering_3pg_2mopy
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_masering_3pg_2mopy
        +guid:f66f1421-7456-444b-ab52-29c78049bb18
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_masering_3pg_2mopy(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7fc0f1f953fb570ee1cb9074f341c91674d8d82445777e74cd463bdc5a93c65d', timeout=600)
    outputsaver.save_output()
