import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 42Page_ctselfon.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:42Page-ctselfon.obj=069e4ae85b8637142f7a6c221dbaa4cd5d4df38bc61bf0e24f5aae7e90631230
    +test_classification:System
    +name: test_pcl5_highvalue_42page_ctselfon
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_42page_ctselfon
        +guid:b614027c-8224-4e93-ae82-d73440ee6c3a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_42page_ctselfon(setup_teardown, printjob, outputsaver):
    printjob.print_verify('069e4ae85b8637142f7a6c221dbaa4cd5d4df38bc61bf0e24f5aae7e90631230', timeout=600)
    outputsaver.save_output()
