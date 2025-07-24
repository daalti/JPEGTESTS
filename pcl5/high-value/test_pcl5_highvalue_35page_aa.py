import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 35Page_aa.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:35Page-aa.obj=6906e4633d2eb46a3dac956594a01140872bf399e103ccf23c6766cf4e292ddc
    +test_classification:System
    +name: test_pcl5_highvalue_35page_aa
    +test:
        +title: test_pcl5_highvalue_35page_aa
        +guid:6cd91e75-3584-42ca-a368-c5a26786cdc6
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_35page_aa(setup_teardown, printjob, outputsaver):
    printjob.print_verify('6906e4633d2eb46a3dac956594a01140872bf399e103ccf23c6766cf4e292ddc', timeout=600)
    outputsaver.save_output()
