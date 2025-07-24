import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PCL5 high value test using **ptdplx2.cht
    +test_tier: 1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-156300
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:ptdplx2.cht=4162ae791c7bd5cc090421a5c23ab379ac5eca85f4a77d3204345d48c93d15b6
    +name:test_pcl5_conf_hv_ptdplx2
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_conf_hv_ptdplx2
        +guid:d4310b02-05f5-44fb-8078-deb9dfb9f6ad
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_conf_hv_ptdplx2(setup_teardown, printjob, outputverifier):
    printjob.print_verify_multi('4162ae791c7bd5cc090421a5c23ab379ac5eca85f4a77d3204345d48c93d15b6',expected_jobs=15,timeout=600)
    outputverifier.save_and_parse_output()
