import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using tgen_ac_3.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tgen_ac_3.obj=43b646118d62ea089af3b2bf600795be13693c6dbaf42f0676312449be896224
    +test_classification:System
    +name: test_pcl5_pcl_arb_clipping_tgen_ac_3
    +test:
        +title: test_pcl5_pcl_arb_clipping_tgen_ac_3
        +guid:e85f8957-0bbe-41d1-a645-e2d58de25c51
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_arb_clipping_tgen_ac_3(setup_teardown, printjob, outputsaver):
    printjob.print_verify('43b646118d62ea089af3b2bf600795be13693c6dbaf42f0676312449be896224', timeout=600)
    outputsaver.save_output()
