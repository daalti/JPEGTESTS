import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using tgen_ac_1.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tgen_ac_1.obj=443db4a499875e2673ba08652ac91575c336db6cde24d391156c82a3b62e4868
    +test_classification:System
    +name: test_pcl5_pcl_arb_clipping_tgen_ac_1
    +test:
        +title: test_pcl5_pcl_arb_clipping_tgen_ac_1
        +guid:8c3eb9f0-c949-409c-a11f-0d12cbf3b04e
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_arb_clipping_tgen_ac_1(setup_teardown, printjob, outputsaver):
    printjob.print_verify('443db4a499875e2673ba08652ac91575c336db6cde24d391156c82a3b62e4868', timeout=600)
    outputsaver.save_output()
