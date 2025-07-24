import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$

    +purpose: pcl5 hpgl using rt_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:rt_igm.obj=c923ecde57c4a63cc33a769235a24c575f49048f0598f2a2cc5ee26f2493fd4a
    +test_classification:System
    +name: test_pcl5_hpgl_vector_rt_igm
    +test:
        +title: test_pcl5_hpgl_vector_rt_igm
        +guid:605a3de1-4fbd-455a-9f0f-6ac28676a937
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_vector_rt_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c923ecde57c4a63cc33a769235a24c575f49048f0598f2a2cc5ee26f2493fd4a', timeout=600)
    outputsaver.save_output()
