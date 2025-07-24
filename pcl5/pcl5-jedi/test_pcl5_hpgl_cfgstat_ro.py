import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ro.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ro.obj=2691671f5708dce4d93cd5443e03320724d621f0c1fbb89755d0aed589857528
    +test_classification:System
    +name: test_pcl5_hpgl_cfgstat_ro
    +test:
        +title: test_pcl5_hpgl_cfgstat_ro
        +guid:affb0799-b181-4eab-887f-1e8accf5a09a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_cfgstat_ro(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2691671f5708dce4d93cd5443e03320724d621f0c1fbb89755d0aed589857528', timeout=600)
    outputsaver.save_output()
