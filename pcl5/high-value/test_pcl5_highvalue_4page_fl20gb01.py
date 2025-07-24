import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 4Page_fl20gb01.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:4Page-fl20gb01.obj=06baa5aa0ebe9c7522bff2e87fdb343de9fa9e6a8fdb016183afbf0f61cfdd87
    +test_classification:System
    +name: test_pcl5_highvalue_4page_fl20gb01
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_4page_fl20gb01
        +guid:181dc250-c686-4cf3-9c5f-306629a6c076
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_highvalue_4page_fl20gb01(setup_teardown, printjob, outputsaver):
    printjob.print_verify('06baa5aa0ebe9c7522bff2e87fdb343de9fa9e6a8fdb016183afbf0f61cfdd87', timeout=200)
    outputsaver.save_output()
