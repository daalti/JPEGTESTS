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
    +external_files:39683-HVA020_49_ALM.prn=5446f465ef0e7c9d4fccc3207a7c0851ed5e11810eb716dc0f5ceeee117a2a50
    +name:test_pcl5_39683_hva020_49_alm_prn
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_39683_hva020_49_alm_prn
        +guid:f6eb750c-4ac3-44a8-ae57-55839f760079
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_39683_hva020_49_alm_prn(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('5446f465ef0e7c9d4fccc3207a7c0851ed5e11810eb716dc0f5ceeee117a2a50')
    outputsaver.save_output()
