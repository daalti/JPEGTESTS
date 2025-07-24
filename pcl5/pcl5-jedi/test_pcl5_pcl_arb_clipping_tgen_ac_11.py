import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using tgen_ac_11.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tgen_ac_11.obj=84b6278537d8f403e6a72a937e0adff1195f98cd94f44480d9def12d7aa546b9
    +test_classification:System
    +name: test_pcl5_pcl_arb_clipping_tgen_ac_11
    +test:
        +title: test_pcl5_pcl_arb_clipping_tgen_ac_11
        +guid:9d2b2a2e-de16-4d10-a708-514c0390e74d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_arb_clipping_tgen_ac_11(setup_teardown, printjob, outputsaver):
    printjob.print_verify('84b6278537d8f403e6a72a937e0adff1195f98cd94f44480d9def12d7aa546b9', timeout=600)
    outputsaver.save_output()
