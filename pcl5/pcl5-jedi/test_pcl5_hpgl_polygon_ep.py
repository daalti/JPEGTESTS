import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ep.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ep.obj=4ef29805747d12a10c99fe242c0a9ec5df45636dec15151742f219ccebc61815
    +test_classification:System
    +name: test_pcl5_hpgl_polygon_ep
    +test:
        +title: test_pcl5_hpgl_polygon_ep
        +guid:7f8b3eb8-d883-4e16-8001-8384aaf1f743
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_polygon_ep(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4ef29805747d12a10c99fe242c0a9ec5df45636dec15151742f219ccebc61815', timeout=600)
    outputsaver.save_output()
