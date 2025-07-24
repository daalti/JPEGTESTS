import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 1Page_ffdupsuppress.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:1Page-ffdupsuppress.obj=0dfeae4719bc03380551ddca94deb34262f64ff840e660a07e34f20ca5317a61
    +test_classification:System
    +name: test_pcl5_lowvaluenew_1page_ffdupsuppress
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_lowvaluenew_1page_ffdupsuppress
        +guid:c90995f2-d41e-46e1-b6f2-dcc40e8ef9cb
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_1page_ffdupsuppress(setup_teardown, printjob, outputsaver):
    printjob.print_verify('0dfeae4719bc03380551ddca94deb34262f64ff840e660a07e34f20ca5317a61', expected_jobs=2, timeout=600)
    outputsaver.save_output()
