import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ip.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ip.obj=b0fd218eb9d0b75d0f5e065e394c4296214cb2d633d24a2078ce367a1aaeaaae
    +test_classification:System
    +name: test_pcl5_hpgl_cfgstat_ip
    +test:
        +title: test_pcl5_hpgl_cfgstat_ip
        +guid:88c2f8a0-34cf-41ef-b654-46a66c2d279b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_cfgstat_ip(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b0fd218eb9d0b75d0f5e065e394c4296214cb2d633d24a2078ce367a1aaeaaae', timeout=600)
    outputsaver.save_output()
