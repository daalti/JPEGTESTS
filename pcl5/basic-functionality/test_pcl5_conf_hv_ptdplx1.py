import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PCL5 high value test using **ptdplx1.cht
    +test_tier: 1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-156300
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:ptdplx1.cht=959beecfe961ae4623cb23329ee033e8605ca0cdaabd3a23fb73a395911a2eae
    +name:test_pcl5_conf_hv_ptdplx1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_conf_hv_ptdplx1
        +guid:a169423f-a6fa-4d61-9a2b-6d9312814f7b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_conf_hv_ptdplx1(setup_teardown, printjob, outputverifier):
    printjob.print_verify('959beecfe961ae4623cb23329ee033e8605ca0cdaabd3a23fb73a395911a2eae', timeout=200)
    outputverifier.save_and_parse_output()