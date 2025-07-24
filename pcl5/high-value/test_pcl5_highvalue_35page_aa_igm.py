import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 35Page_aa_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:35Page-aa_igm.obj=5b3d32983bbf91f10014571df2a156968dac5b7ab69855607f6896cc8582692d
    +test_classification:System
    +name: test_pcl5_highvalue_35page_aa_igm
    +test:
        +title: test_pcl5_highvalue_35page_aa_igm
        +guid:828e2e7d-9fc0-471e-ac3c-73911208a488
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_35page_aa_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5b3d32983bbf91f10014571df2a156968dac5b7ab69855607f6896cc8582692d', timeout=600)
    outputsaver.save_output()
