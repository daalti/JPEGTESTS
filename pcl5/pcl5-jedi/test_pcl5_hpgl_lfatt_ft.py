import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ft.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ft.obj=96e8e1e3032a89474e49374d059eab93ea458d2da8da0e8ad9263cd28f3ed8ee
    +test_classification:System
    +name: test_pcl5_hpgl_lfatt_ft
    +test:
        +title: test_pcl5_hpgl_lfatt_ft
        +guid:75e4bcb1-39fa-49cc-bf4e-e817310aa52f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_lfatt_ft(setup_teardown, printjob, outputsaver):
    printjob.print_verify('96e8e1e3032a89474e49374d059eab93ea458d2da8da0e8ad9263cd28f3ed8ee', timeout=600)
    outputsaver.save_output()
