import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using pjlfontsource.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:800
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:pjlfontsource.pcl=5f2c50c1c021bc5569dc2cb2e4a82a9b052b7d91c8db62e1a8a578f669566ce6
    +test_classification:System
    +name: test_pcl5_testfiles_pjl_pjlfontsource
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_pjl_pjlfontsource
        +guid:aff49966-1a5c-4496-b45b-d92bead236b6
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_testfiles_pjl_pjlfontsource(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5f2c50c1c021bc5569dc2cb2e4a82a9b052b7d91c8db62e1a8a578f669566ce6', timeout=600)
    outputsaver.save_output()
