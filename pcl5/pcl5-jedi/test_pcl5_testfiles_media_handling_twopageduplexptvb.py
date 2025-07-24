import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using TwoPageDuplexPTVB.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:TwoPageDuplexPTVB.pcl=841d8017bc6875b5ea697705e5866752653a18c914a7af556898c38c467be9a9
    +test_classification:System
    +name: test_pcl5_testfiles_media_handling_twopageduplexptvb
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_media_handling_twopageduplexptvb
        +guid:9b64fbb5-d20b-427d-b257-4014373664cb
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_media_handling_twopageduplexptvb(setup_teardown, printjob, outputsaver):
    printjob.print_verify('841d8017bc6875b5ea697705e5866752653a18c914a7af556898c38c467be9a9', timeout=600)
    outputsaver.save_output()
